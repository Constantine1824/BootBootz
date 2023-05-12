from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Core.permissions import IsVerified
from .serializers import OrderSerializer,OrderCreationSerializer

class OrderAPIView(APIView):
    permission_classes = [IsVerified,IsAuthenticated]
    
    def post(self,request):
        data = request.data
        serializer = OrderCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    def get(self,request):
        user = request.user
        order = Order.objects.filter(user=user)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
# Create your views here.
