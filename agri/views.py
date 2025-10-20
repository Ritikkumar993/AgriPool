from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Shipment, Crop
from .serializers import ShipmentSerializer, CropSerializer
from .utils import simple_pool

class CreateShipmentView(APIView):
    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListShipmentsView(APIView):
    def get(self, request):
        shipments = Shipment.objects.filter(status='open')
        data = [ShipmentSerializer(s).data for s in shipments]
        return Response(data)

from rest_framework.decorators import api_view

@api_view(['GET'])
def pool_shipments(request):
    radius_km = float(request.GET.get('radius_km', 10))
    shipments = Shipment.objects.filter(status='open')
    pools = simple_pool(shipments, radius_km=radius_km)
    result = []
    for group in pools:
        result.append({
            'shipment_ids': [str(s.id) for s in group],
            'total_qty_kg': sum(s.quantity_kg for s in group),
            'centroid': {
                'lat': sum(s.pickup_lat for s in group)/len(group),
                'lon': sum(s.pickup_lon for s in group)/len(group),
            }
        })
    return Response(result)
