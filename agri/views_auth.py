from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Farmer
import hashlib

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone', '')
        village = request.data.get('village', '')

        if not username or not password:
            return Response({'error': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Farmer.objects.filter(username=username).first():
            return Response({'error': 'username exists'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        farmer = Farmer(username=username, password=hashed_password, phone=phone, village=village).save()
        return Response({'message': 'registered', 'farmer_id': str(farmer.id)}, status=status.HTTP_201_CREATED)
