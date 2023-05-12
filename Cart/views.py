from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartSerializer,CartCreationSerializer
from .models import Cart
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.test import APISimpleTestCase

class AddToCartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        product_id = request.data['product_id']
        user = request.user
        cart = Cart.objects.get(user=user)
        if cart is not None:
            cart.products.add(product_id)
            cart.save()
            serializer= CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart = Cart.objects.create(user=user)
            cart.products.add(product_id)
            cart.save()
            serializer= CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# class DetailCartAPIView(RetrieveAPIView):
#     queryset = Cart
#     serializer_class = CartSerializer

#     def get_object(self):
#         obj = self.queryset.objects.get(user=self.request.user,)
#         return obj

class DetailCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart_obj = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart_obj)
        if cart_obj is not None:
            return Response(serializer.data)


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
