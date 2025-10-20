from django.core.management.base import BaseCommand
from agri.models import Farmer, Transporter, Parcel, Crop, Shipment, TransportOffer
from datetime import datetime, timedelta
import hashlib

class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating demo data...')
        
        # Create crops
        crops_data = [
            {'name': 'Wheat', 'season': 'Rabi'},
            {'name': 'Rice', 'season': 'Kharif'},
            {'name': 'Cotton', 'season': 'Kharif'},
            {'name': 'Sugarcane', 'season': 'Year-round'},
            {'name': 'Tomato', 'season': 'Year-round'},
            {'name': 'Potato', 'season': 'Rabi'},
        ]
        
        for crop_data in crops_data:
            if not Crop.objects.filter(name=crop_data['name']).first():
                Crop(**crop_data).save()
                self.stdout.write(f'Created crop: {crop_data["name"]}')
        
        # Create demo farmers
        password = hashlib.sha256('demo123'.encode()).hexdigest()
        
        farmers_data = [
            {'username': 'ramesh_farmer', 'email': 'ramesh@example.com', 'phone': '9876543210', 'village': 'Pune'},
            {'username': 'priya_farmer', 'email': 'priya@example.com', 'phone': '9876543211', 'village': 'Nashik'},
            {'username': 'suresh_farmer', 'email': 'suresh@example.com', 'phone': '9876543212', 'village': 'Satara'},
        ]
        
        farmers = []
        for farmer_data in farmers_data:
            if not Farmer.objects.filter(username=farmer_data['username']).first():
                farmer = Farmer(**farmer_data, password=password)
                farmer.save()
                farmers.append(farmer)
                self.stdout.write(f'Created farmer: {farmer_data["username"]}')
        
        # Create demo transporters
        transporters_data = [
            {'username': 'transport_raj', 'email': 'raj@transport.com', 'phone': '9876543220', 
             'vehicle_type': 'truck', 'vehicle_capacity_kg': 5000},
            {'username': 'transport_vijay', 'email': 'vijay@transport.com', 'phone': '9876543221', 
             'vehicle_type': 'tempo', 'vehicle_capacity_kg': 2000},
        ]
        
        transporters = []
        for trans_data in transporters_data:
            if not Transporter.objects.filter(username=trans_data['username']).first():
                transporter = Transporter(**trans_data, password=password)
                transporter.save()
                transporters.append(transporter)
                self.stdout.write(f'Created transporter: {trans_data["username"]}')
        
        # Create demo parcels
        if farmers:
            parcels_data = [
                {'name': 'North Field', 'area_hectare': 2.5, 'soil_type': 'loam', 'latitude': 18.5204, 'longitude': 73.8567},
                {'name': 'South Field', 'area_hectare': 3.0, 'soil_type': 'clay', 'latitude': 18.5304, 'longitude': 73.8667},
            ]
            
            for i, parcel_data in enumerate(parcels_data):
                farmer = farmers[i % len(farmers)]
                if not Parcel.objects.filter(farmer=farmer, name=parcel_data['name']).first():
                    Parcel(farmer=farmer, **parcel_data).save()
                    self.stdout.write(f'Created parcel: {parcel_data["name"]}')
        
        # Create demo transport offers
        if transporters:
            offers_data = [
                {'from_location': 'Pune', 'to_location': 'Mumbai', 'capacity_kg': 5000, 'price_per_kg': 5.5},
                {'from_location': 'Nashik', 'to_location': 'Mumbai', 'capacity_kg': 2000, 'price_per_kg': 6.0},
                {'from_location': 'Satara', 'to_location': 'Pune', 'capacity_kg': 3000, 'price_per_kg': 4.5},
            ]
            
            for i, offer_data in enumerate(offers_data):
                transporter = transporters[i % len(transporters)]
                offer_data['available_date'] = datetime.now() + timedelta(days=i+1)
                TransportOffer(transporter=transporter, **offer_data).save()
                self.stdout.write(f'Created transport offer: {offer_data["from_location"]} to {offer_data["to_location"]}')
        
        self.stdout.write(self.style.SUCCESS('Demo data populated successfully!'))
        self.stdout.write('Demo credentials: username=ramesh_farmer, password=demo123')
