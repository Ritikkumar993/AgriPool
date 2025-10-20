from rest_framework import serializers
from .models import Farmer, Crop, Shipment

class FarmerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    phone = serializers.CharField(max_length=15, required=False)
    village = serializers.CharField(max_length=128, required=False)

    def create(self, validated_data):
        return Farmer(**validated_data).save()

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class CropSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return Crop(**validated_data).save()

class ShipmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    farmer = serializers.CharField()
    crop = serializers.CharField()
    quantity_kg = serializers.FloatField()
    pickup_location = serializers.CharField(max_length=128)
    pickup_lat = serializers.FloatField(required=False)
    pickup_lon = serializers.FloatField(required=False)
    destination_market = serializers.CharField(max_length=128)
    ready_from = serializers.DateTimeField()
    ready_to = serializers.DateTimeField()
    status = serializers.CharField(max_length=32, default='open')

    def create(self, validated_data):
        farmer_id = validated_data.pop('farmer')
        crop_id = validated_data.pop('crop')
        
        farmer = Farmer.objects.get(id=farmer_id)
        crop = Crop.objects.get(id=crop_id)
        
        return Shipment(farmer=farmer, crop=crop, **validated_data).save()
