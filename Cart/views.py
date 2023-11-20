from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartSerializer,CartCreationSerializer
from .models import Cart
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.test import APISimpleTestCase

class CartApiView(APIView):
    """
    This endpoint is responsible for adding items to cart. It accepts multiple products at once
    The endpoint handles the following:
    - GET request to get the cart
    - POST - To bulk update the cart

    Returns
    - POST: A JSON response of the sent data
    - GET: A JSON response of the cart and all cart items 
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        """This endpoint handles the POST request and requires a list of products to be added to the cart
        """
        cart = Cart.objects.get_or_create(user=request.user)
        serializer = CartCreationSerializer(data=request.data, context={'cart' : cart})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                "status" : "added to cart",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
    def get(self, request):
        """
        This handles the GET request and retrieves cart data
        """
        queryset = Cart.objects.get(user=request.user)
        serializer = CartSerializer(queryset)
        response = {
            "status" : "retrieved",
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class DeleteFromCartAPIView(APIView):
    """This view should receive a list of items to be removed from the cart.
    The frontend data should compulsorily be a list or this endpoint should be sent every time a user 
    decides to delete an item from their cart.
    For now it will be designed to be called every time a user deletes.
    """
    def post(self,request):
       product_id = request.data['product_id']
       cart = Cart.objects.get(user=request.user)
       if cart is not None:
           cart.products.remove(product_id)
           cart.save()
           return Response({
               "detail" : "Succesfully removed"
           }, status=status.HTTP_200_OK)
       raise APIException({
           'detail' : "Cart is None"
       }, code=status.HTTP_400_BAD_REQUEST)
    
class ClearCartAPIView(APIView):
    pass
# Create your views here.
