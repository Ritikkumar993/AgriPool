from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField, EmailField, BooleanField
from datetime import datetime

class Farmer(Document):
    username = StringField(required=True, unique=True)
    email = EmailField()
    phone = StringField(max_length=15)
    village = StringField(max_length=128)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.username

class Transporter(Document):
    username = StringField(required=True, unique=True)
    email = EmailField()
    phone = StringField(max_length=15)
    vehicle_type = StringField(max_length=64)
    vehicle_capacity_kg = FloatField()
    vehicle_number = StringField(max_length=20)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.username

class Crop(Document):
    name = StringField(max_length=64, unique=True)
    season = StringField(max_length=32)

    def __str__(self):
        return self.name

class Shipment(Document):
    """Farmer's request to transport produce to market"""
    farmer = ReferenceField(Farmer)
    crop = ReferenceField(Crop)
    quantity_kg = FloatField()
    pickup_location = StringField(max_length=128)
    pickup_lat = FloatField()
    pickup_lon = FloatField()
    destination_market = StringField(max_length=128)
    ready_from = DateTimeField()
    ready_to = DateTimeField()
    status = StringField(max_length=32, default='open')  # open, pooled, booked, completed
    transport_offer = ReferenceField('TransportOffer', null=True)
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"Shipment {self.id} - {self.crop.name} - {self.quantity_kg}kg"

class TransportOffer(Document):
    """Transporter's available route and capacity"""
    transporter = ReferenceField(Transporter)
    from_location = StringField(max_length=128)
    to_location = StringField(max_length=128)
    available_date = DateTimeField()
    capacity_kg = FloatField()
    available_capacity_kg = FloatField()  # Remaining capacity
    price_per_kg = FloatField()
    status = StringField(max_length=32, default='available')  # available, partial, full, completed
    pooled_shipments = StringField()  # Comma-separated shipment IDs
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.from_location} to {self.to_location}"

class Booking(Document):
    """Booking of transport by farmer"""
    shipment = ReferenceField(Shipment)
    transport_offer = ReferenceField(TransportOffer)
    farmer = ReferenceField(Farmer)
    transporter = ReferenceField(Transporter)
    booking_date = DateTimeField(default=datetime.utcnow)
    
    # Pricing and negotiation
    original_price_per_kg = FloatField()  # Transporter's original price
    proposed_price_per_kg = FloatField()  # Farmer's proposed price
    final_price_per_kg = FloatField()  # Agreed price
    estimated_cost = FloatField()  # Based on final price
    
    # Negotiation status
    negotiation_status = StringField(max_length=32, default='pending')  # pending, accepted, counter_offered, rejected
    counter_offer_price = FloatField()  # Transporter's counter offer
    negotiation_notes = StringField()  # Reason for counter/rejection
    
    # Booking status
    status = StringField(max_length=32, default='pending')  # pending, confirmed, in_transit, completed, cancelled
    notes = StringField()
    
    def __str__(self):
        return f"Booking {self.id} - {self.farmer.username}"

class PooledTransport(Document):
    """Represents a pooled transport with multiple shipments"""
    transport_offer = ReferenceField(TransportOffer)
    bookings = StringField()  # Comma-separated booking IDs
    total_quantity_kg = FloatField()
    total_cost = FloatField()
    status = StringField(max_length=32, default='pending')  # pending, confirmed, in_transit, completed
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"Pool {self.id} - {self.total_quantity_kg}kg"

class Feedback(Document):
    name = StringField(max_length=128)
    email = EmailField()
    message = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"Feedback from {self.name}"
