"""
Capacity Manager - Ensures ACID properties for transport capacity management
"""
from .models import TransportOffer, Booking, Shipment

class CapacityManager:
    """
    Centralized capacity management to ensure consistency
    """
    
    @staticmethod
    def check_availability(transport_offer, required_kg):
        """
        Check if transport has enough capacity
        Returns: (bool, str) - (is_available, message)
        """
        if not transport_offer.available_capacity_kg:
            # Initialize if not set
            transport_offer.available_capacity_kg = transport_offer.capacity_kg
            transport_offer.save()
        
        available = transport_offer.available_capacity_kg
        
        if available >= required_kg:
            return True, f"{available} kg available"
        else:
            return False, f"Only {available} kg available, need {required_kg} kg"
    
    @staticmethod
    def reserve_capacity(booking):
        """
        Reserve capacity when booking is confirmed
        This is an atomic operation
        """
        transport_offer = booking.transport_offer
        shipment = booking.shipment
        required_kg = shipment.quantity_kg
        
        # Reload to get latest data (prevent race conditions)
        transport_offer.reload()
        
        # Check availability
        is_available, message = CapacityManager.check_availability(transport_offer, required_kg)
        
        if not is_available:
            raise ValueError(f"Insufficient capacity: {message}")
        
        # Atomic update
        transport_offer.available_capacity_kg -= required_kg
        
        # Update status based on remaining capacity
        if transport_offer.available_capacity_kg <= 0:
            transport_offer.status = 'full'
        elif transport_offer.available_capacity_kg < transport_offer.capacity_kg:
            transport_offer.status = 'partial'
        else:
            transport_offer.status = 'available'
        
        transport_offer.save()
        
        # Update shipment
        shipment.status = 'booked'
        shipment.transport_offer = transport_offer
        shipment.save()
        
        # Update booking
        booking.status = 'confirmed'
        booking.save()
        
        return True
    
    @staticmethod
    def release_capacity(booking):
        """
        Release capacity when booking is cancelled/rejected
        This is an atomic operation
        """
        transport_offer = booking.transport_offer
        shipment = booking.shipment
        released_kg = shipment.quantity_kg
        
        # Only release if booking was confirmed (capacity was reserved)
        if booking.status == 'confirmed':
            # Reload to get latest data
            transport_offer.reload()
            
            # Atomic update
            transport_offer.available_capacity_kg += released_kg
            
            # Ensure we don't exceed total capacity
            if transport_offer.available_capacity_kg > transport_offer.capacity_kg:
                transport_offer.available_capacity_kg = transport_offer.capacity_kg
            
            # Update status
            if transport_offer.available_capacity_kg >= transport_offer.capacity_kg:
                transport_offer.status = 'available'
            elif transport_offer.available_capacity_kg > 0:
                transport_offer.status = 'partial'
            
            transport_offer.save()
        
        # Update shipment
        shipment.status = 'open'
        shipment.transport_offer = None
        shipment.save()
        
        # Update booking
        booking.status = 'cancelled'
        booking.save()
        
        return True
    
    @staticmethod
    def get_available_capacity(transport_offer):
        """
        Get current available capacity
        """
        if not transport_offer.available_capacity_kg:
            return transport_offer.capacity_kg
        return transport_offer.available_capacity_kg
    
    @staticmethod
    def validate_booking(transport_offer, shipment):
        """
        Validate if booking can be made
        Returns: (bool, str) - (is_valid, message)
        """
        # Check if transport is available
        if transport_offer.status == 'full':
            return False, "Transport is fully booked"
        
        # Check capacity
        required_kg = shipment.quantity_kg
        is_available, message = CapacityManager.check_availability(transport_offer, required_kg)
        
        if not is_available:
            return False, message
        
        # Check if shipment is already booked
        if shipment.status == 'booked':
            return False, "Shipment is already booked"
        
        return True, "Booking is valid"
    
    @staticmethod
    def initialize_capacity(transport_offer):
        """
        Initialize available capacity if not set
        """
        if not transport_offer.available_capacity_kg:
            transport_offer.available_capacity_kg = transport_offer.capacity_kg
            transport_offer.status = 'available'
            transport_offer.save()
        return transport_offer.available_capacity_kg
