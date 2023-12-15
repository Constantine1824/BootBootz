from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItems, models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Core.permissions import IsVerified
from Cart.models import Cart
from .serializers import OrderSerializer,OrderCreationSerializer

class OrderAPIView(APIView):
    permission_classes = [IsVerified,IsAuthenticated]
    
    def post(self,request):
        """
        Post a request to create a new order.

        Parameters:
            - request: The HTTP request object.

        Returns:
            - A Response object with the created order ID and a status code of 201 (Created).
        """
        cart = Cart.objects.get(user=request.user) #Get the cart instance first
        order_obj = Order.objects.create(user=request.user)
        order_items = [OrderItems(order=order_obj, product=i.product, quantity=i.boot) for i in cart.cartItems.all()]
        OrderItems.objects.bulk_create(order_items)
        order_obj.total_price = order_obj.orderItems.product.aggregate(models.Sum('price'))['price__sum'] + order_obj.delivery_fee
        return Response({
            "order_id":order_obj.tracking_id
            },
            status=status.HTTP_201_CREATED)  

        
    def get(self,request):
        """
        Retrieves the orders associated with the specified user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The serialized data of the retrieved orders.
        """
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
# Create your views here.
