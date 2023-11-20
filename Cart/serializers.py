from rest_framework.serializers import ModelSerializer,CharField,SerializerMethodField,Field
from Core.serializers import BootsSerializer
from .models import Cart, CartItems
from rest_framework.fields import Field
from rest_framework.exceptions import APIException
from Core.models import Boots, Variants
from Core.serializers import BootsSerializer
from Auth.models import User
from Auth.serializers import UserSerializer
from collections import OrderedDict


class VariantSerializer(ModelSerializer):
    boot_detail = BootsSerializer(read_only=True, source='boot')

    class Meta:
        model = Variants
        fields = ['boot', 'color']




class CartItemsSerializer(ModelSerializer):
    boot_details = VariantSerializer(source='boot') 
    class Meta:
        model = CartItems
        fields = '__all__'


class CartSerializer(ModelSerializer):
    user = UserSerializer()
    cart_items = CartItemsSerializer(many=True, source='cartItems', read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart_items']

class CartCreationSerializer(ModelSerializer):
    cart = CartSerializer(read_only=True)
    class Meta:
        model = CartItems
        fields = '__all__'


    def bulk_create(self, validated_data, cart):
        items = [self.Meta.model(cart=cart,**item) for item in validated_data]
        cartItems = CartItems.objects.bulk_create(items)
        return cartItems


    def create(self, validated_data):
        cart = self.context['cart']
        try:
            cartItems = self.bulk_create(validated_data, cart)
            return cartItems
        except Exception as e:
           print(e)
           raise APIException('An unknown error occured')