from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .models import Farmer, Transporter, Crop, Shipment, TransportOffer, Feedback, Booking
from .capacity_manager import CapacityManager
from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'farmer')
        
        hashed_password = hash_password(password)
        
        if user_type == 'farmer':
            user = Farmer.objects.filter(username=username, password=hashed_password).first()
        else:
            user = Transporter.objects.filter(username=username, password=hashed_password).first()
        
        if user:
            request.session['user_id'] = str(user.id)
            request.session['user_type'] = user_type
            request.session['username'] = user.username
            
            if user_type == 'farmer':
                return redirect('farmer_dashboard')
            else:
                return redirect('transporter_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'farmer')
        
        hashed_password = hash_password(password)
        
        try:
            if user_type == 'farmer':
                village = request.POST.get('village', '')
                if Farmer.objects.filter(username=username).first():
                    return render(request, 'register.html', {'error': 'Username already exists'})
                
                farmer = Farmer(
                    username=username,
                    email=email,
                    phone=phone,
                    village=village,
                    password=hashed_password
                )
                farmer.save()
                user_id = str(farmer.id)
            else:
                vehicle_type = request.POST.get('vehicle_type', 'truck')
                vehicle_capacity = float(request.POST.get('vehicle_capacity', 0))
                
                if Transporter.objects.filter(username=username).first():
                    return render(request, 'register.html', {'error': 'Username already exists'})
                
                transporter = Transporter(
                    username=username,
                    email=email,
                    phone=phone,
                    vehicle_type=vehicle_type,
                    vehicle_capacity_kg=vehicle_capacity,
                    password=hashed_password
                )
                transporter.save()
                user_id = str(transporter.id)
            
            request.session['user_id'] = user_id
            request.session['user_type'] = user_type
            request.session['username'] = username
            
            if user_type == 'farmer':
                return redirect('farmer_dashboard')
            else:
                return redirect('transporter_dashboard')
                
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})
    
    return render(request, 'register.html')

def logout_view(request):
    request.session.flush()
    return redirect('home')

def farmer_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'farmer':
        return redirect('login')
    
    farmer = Farmer.objects.get(id=user_id)
    shipments = Shipment.objects.filter(farmer=farmer).order_by('-created_at')
    
    # Calculate statistics
    open_shipments = shipments.filter(status='open').count()
    pooled_shipments = shipments.filter(status='pooled').count()
    completed_shipments = shipments.filter(status='completed').count()
    
    # Calculate total quantity and potential savings
    total_quantity = sum([s.quantity_kg for s in shipments])
    
    context = {
        'farmer': farmer,
        'shipments': shipments[:10],  # Show last 10
        'total_shipments': shipments.count(),
        'open_shipments': open_shipments,
        'pooled_shipments': pooled_shipments,
        'completed_shipments': completed_shipments,
        'total_quantity': total_quantity,
        'user_id': user_id,
        'user_type': 'farmer'
    }
    return render(request, 'farmer_dashboard.html', context)

def transporter_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'transporter':
        return redirect('login')
    
    transporter = Transporter.objects.get(id=user_id)
    offers = TransportOffer.objects.filter(transporter=transporter).order_by('-created_at')
    
    context = {
        'transporter': transporter,
        'offers': offers,
        'offers_count': offers.filter(status='available').count(),
        'completed_trips': offers.filter(status='completed').count(),
        'user_id': user_id,
        'user_type': 'transporter'
    }
    return render(request, 'transporter_dashboard.html', context)



@require_http_methods(["GET", "POST"])
def create_shipment(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'farmer':
        return redirect('login')
    
    farmer = Farmer.objects.get(id=user_id)
    crops = Crop.objects.all()
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        quantity = float(request.POST.get('quantity_kg'))
        pickup_location = request.POST.get('pickup_location')
        pickup_lat = float(request.POST.get('pickup_lat', 0))
        pickup_lon = float(request.POST.get('pickup_lon', 0))
        destination = request.POST.get('destination_market')
        ready_from = request.POST.get('ready_from')
        ready_to = request.POST.get('ready_to')
        
        crop = Crop.objects.get(id=crop_id)
        
        shipment = Shipment(
            farmer=farmer,
            crop=crop,
            quantity_kg=quantity,
            pickup_location=pickup_location,
            pickup_lat=pickup_lat,
            pickup_lon=pickup_lon,
            destination_market=destination,
            ready_from=datetime.fromisoformat(ready_from),
            ready_to=datetime.fromisoformat(ready_to)
        )
        shipment.save()
        return redirect('farmer_dashboard')
    
    context = {
        'crops': crops,
        'user_id': user_id,
        'user_type': 'farmer'
    }
    return render(request, 'create_shipment.html', context)



def transport_list(request):
    # Get all offers (not just 'available' to show partial too)
    offers = TransportOffer.objects.filter(status__in=['available', 'partial']).order_by('-created_at')
    
    # Initialize capacity for all offers
    for offer in offers:
        CapacityManager.initialize_capacity(offer)
    
    # Apply filters
    from_loc = request.GET.get('from')
    to_loc = request.GET.get('to')
    capacity = request.GET.get('capacity')
    
    if from_loc:
        offers = offers.filter(from_location__icontains=from_loc)
    if to_loc:
        offers = offers.filter(to_location__icontains=to_loc)
    if capacity:
        # Filter by available capacity, not total capacity
        offers = [o for o in offers if CapacityManager.get_available_capacity(o) >= float(capacity)]
    
    context = {
        'offers': offers,
        'user_id': request.session.get('user_id'),
        'user_type': request.session.get('user_type')
    }
    return render(request, 'transport_list.html', context)

@require_http_methods(["GET", "POST"])
def add_transport_offer(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'transporter':
        return redirect('login')
    
    if request.method == 'POST':
        transporter = Transporter.objects.get(id=user_id)
        from_loc = request.POST.get('from_location')
        to_loc = request.POST.get('to_location')
        capacity = float(request.POST.get('capacity_kg'))
        price = float(request.POST.get('price_per_kg'))
        available_date = request.POST.get('available_date')
        
        offer = TransportOffer(
            transporter=transporter,
            from_location=from_loc,
            to_location=to_loc,
            capacity_kg=capacity,
            available_capacity_kg=capacity,  # Initialize with full capacity
            price_per_kg=price,
            available_date=datetime.fromisoformat(available_date)
        )
        offer.save()
        return redirect('transporter_dashboard')
    
    return render(request, 'add_transport_offer.html', {'user_id': user_id, 'user_type': 'transporter'})

@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        feedback = Feedback(name=name, email=email, message=message)
        feedback.save()
        
        return render(request, 'contact.html', {
            'success': True,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type')
        })
    
    return render(request, 'contact.html', {
        'user_id': request.session.get('user_id'),
        'user_type': request.session.get('user_type')
    })


@require_http_methods(["GET", "POST"])
def book_transport(request, offer_id):
    """Book a transport offer"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'farmer':
        return redirect('login')
    
    farmer = Farmer.objects.get(id=user_id)
    transport_offer = TransportOffer.objects.get(id=offer_id)
    
    # Get farmer's open shipments
    shipments = Shipment.objects.filter(farmer=farmer, status='open')
    
    if request.method == 'POST':
        shipment_id = request.POST.get('shipment_id')
        notes = request.POST.get('notes', '')
        proposed_price = request.POST.get('proposed_price_per_kg')
        
        shipment = Shipment.objects.get(id=shipment_id)
        
        # VALIDATION: Check if booking is valid
        is_valid, message = CapacityManager.validate_booking(transport_offer, shipment)
        if not is_valid:
            context = {
                'transport_offer': transport_offer,
                'shipments': shipments,
                'error': message,
                'user_id': user_id,
                'user_type': 'farmer'
            }
            return render(request, 'book_transport.html', context)
        
        # Get prices
        original_price = transport_offer.price_per_kg
        
        # If farmer proposes a price, use it; otherwise use original
        if proposed_price and float(proposed_price) > 0:
            proposed_price = float(proposed_price)
            final_price = proposed_price
            negotiation_status = 'pending' if proposed_price < original_price else 'accepted'
        else:
            proposed_price = original_price
            final_price = original_price
            negotiation_status = 'accepted'
        
        # Calculate estimated cost
        estimated_cost = shipment.quantity_kg * final_price
        
        # Create booking
        booking = Booking(
            shipment=shipment,
            transport_offer=transport_offer,
            farmer=farmer,
            transporter=transport_offer.transporter,
            original_price_per_kg=original_price,
            proposed_price_per_kg=proposed_price,
            final_price_per_kg=final_price,
            estimated_cost=estimated_cost,
            negotiation_status=negotiation_status,
            notes=notes,
            status='pending'
        )
        booking.save()
        
        # ATOMIC OPERATION: Reserve capacity if negotiation is auto-accepted
        if negotiation_status == 'accepted':
            try:
                CapacityManager.reserve_capacity(booking)
            except ValueError as e:
                # Capacity not available, delete booking
                booking.delete()
                context = {
                    'transport_offer': transport_offer,
                    'shipments': shipments,
                    'error': str(e),
                    'user_id': user_id,
                    'user_type': 'farmer'
                }
                return render(request, 'book_transport.html', context)
        else:
            # Keep shipment as pending until negotiation is accepted
            shipment.status = 'pending_booking'
            shipment.save()
        
        return redirect('booking_confirmation', booking_id=str(booking.id))
    
    context = {
        'transport_offer': transport_offer,
        'shipments': shipments,
        'user_id': user_id,
        'user_type': 'farmer'
    }
    return render(request, 'book_transport.html', context)

def booking_confirmation(request, booking_id):
    """Show booking confirmation"""
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    booking = Booking.objects.get(id=booking_id)
    
    context = {
        'booking': booking,
        'user_id': user_id,
        'user_type': request.session.get('user_type')
    }
    return render(request, 'booking_confirmation.html', context)

def my_bookings(request):
    """View all bookings for farmer"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'farmer':
        return redirect('login')
    
    farmer = Farmer.objects.get(id=user_id)
    bookings = Booking.objects.filter(farmer=farmer).order_by('-booking_date')
    
    context = {
        'bookings': bookings,
        'user_id': user_id,
        'user_type': 'farmer'
    }
    return render(request, 'my_bookings.html', context)

def transporter_bookings(request):
    """View all bookings for transporter"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'transporter':
        return redirect('login')
    
    transporter = Transporter.objects.get(id=user_id)
    bookings = Booking.objects.filter(transporter=transporter).order_by('-booking_date')
    
    context = {
        'bookings': bookings,
        'user_id': user_id,
        'user_type': 'transporter'
    }
    return render(request, 'transporter_bookings.html', context)

@require_http_methods(["POST"])
def update_booking_status(request, booking_id):
    """Update booking status (for transporter)"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'transporter':
        return redirect('login')
    
    booking = Booking.objects.get(id=booking_id)
    new_status = request.POST.get('status')
    
    if new_status in ['confirmed', 'in_transit', 'completed', 'cancelled']:
        booking.status = new_status
        booking.save()
        
        # Update shipment status
        if new_status == 'completed':
            booking.shipment.status = 'completed'
            booking.shipment.save()
    
    return redirect('transporter_bookings')


@require_http_methods(["POST"])
def respond_to_negotiation(request, booking_id):
    """Transporter responds to price negotiation"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'transporter':
        return redirect('login')
    
    booking = Booking.objects.get(id=booking_id)
    action = request.POST.get('action')  # accept, reject, counter
    
    if action == 'accept':
        # Accept farmer's proposed price
        booking.negotiation_status = 'accepted'
        booking.final_price_per_kg = booking.proposed_price_per_kg
        booking.estimated_cost = booking.shipment.quantity_kg * booking.final_price_per_kg
        booking.save()
        
        # ATOMIC OPERATION: Reserve capacity
        try:
            CapacityManager.reserve_capacity(booking)
        except ValueError as e:
            # Capacity not available anymore
            booking.negotiation_status = 'rejected'
            booking.negotiation_notes = f"Capacity no longer available: {str(e)}"
            booking.status = 'cancelled'
            booking.save()
            booking.shipment.status = 'open'
            booking.shipment.save()
        
    elif action == 'reject':
        # ATOMIC OPERATION: Release capacity if was reserved
        CapacityManager.release_capacity(booking)
        
        # Update negotiation status
        booking.negotiation_status = 'rejected'
        booking.negotiation_notes = request.POST.get('notes', 'Price too low')
        booking.save()
        
    elif action == 'counter':
        # Make counter offer
        counter_price = float(request.POST.get('counter_price'))
        booking.negotiation_status = 'counter_offered'
        booking.counter_offer_price = counter_price
        booking.final_price_per_kg = counter_price
        booking.estimated_cost = booking.shipment.quantity_kg * counter_price
        booking.negotiation_notes = request.POST.get('notes', '')
        booking.save()
    
    return redirect('transporter_bookings')

@require_http_methods(["POST"])
def respond_to_counter_offer(request, booking_id):
    """Farmer responds to transporter's counter offer"""
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'farmer':
        return redirect('login')
    
    booking = Booking.objects.get(id=booking_id)
    action = request.POST.get('action')  # accept, reject
    
    if action == 'accept':
        # Accept counter offer
        booking.negotiation_status = 'accepted'
        booking.save()
        
        # ATOMIC OPERATION: Reserve capacity
        try:
            CapacityManager.reserve_capacity(booking)
        except ValueError as e:
            # Capacity not available anymore
            booking.negotiation_status = 'rejected'
            booking.negotiation_notes = f"Capacity no longer available: {str(e)}"
            booking.status = 'cancelled'
            booking.save()
            booking.shipment.status = 'open'
            booking.shipment.save()
        
    elif action == 'reject':
        # ATOMIC OPERATION: Release capacity if was reserved
        CapacityManager.release_capacity(booking)
        
        # Update negotiation status
        booking.negotiation_status = 'rejected'
        booking.save()
    
    return redirect('my_bookings')
