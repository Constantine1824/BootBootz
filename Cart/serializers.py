from rest_framework.serializers import ModelSerializer,CharField,SerializerMethodField,Field
from Core.serializers import ProductsSerializer
from .models import Cart
from rest_framework.fields import Field
from rest_framework.exceptions import APIException
from Core.models import Products
from Auth.models import User
from collections import OrderedDict


class CartField(Field):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        names = []
        for i in range(len(data)):
            print(data[i]['name'])
            names.append(data[i]['name'])
         # Get the list of products
        Boots = [Products.objects.get(name =name_) for name_ in names]
        print(Boots)
        # Serialize the Boots, sounds crazy but i have few choices
        serializer = ProductsSerializer(Boots,many=True)
        # Return the list as an ordered dict
        return serializer.data

    def to_representation(self, name):
        print(name)
        # Get the list of products
        Boots = [Products.objects.get(name =name_) for name_ in name]
        print(Boots)
        # Return the list as an ordered dict

        return OrderedDict(Boots)

class CartProducts(ModelSerializer):

    class Meta:
        model = Products
        fields = ['name']

class CartCreationSerializer(ModelSerializer):
    user = CharField()
    class Meta:
        model = Cart
        fields = '__all__'


    def create(self, validated_data):
        username = validated_data.pop('user',None)
        user = User.objects.get(username=username)
        try:
            cart = Cart.objects.get(user=user)
            
            products= validated_data['products']
            #In this case we update the cart "
            cart.products.set(products)
            cart.save()
            return cart
        except Exception as e:
            print(e)
            cart = Cart.objects.create(user=user)
            products = validated_data['products']
            cart.products.add(products)
            cart.save()
            print(validated_data)
            return cart
        
        # Create a new cart instance
        

        # products = validated_data.pop('products')
        # print(products[0]['name'])
        # instance = self.Meta.model.objects.create(user=user)
        # print("PRODUCTS:", products)
        # for field_,value in products.items():
        #     field = getattr(instance,field_)
        #     field.set(value)
        # instance.save()
        # for i in range(len(products)):
        #     name = products[i]['name']
        #     product_instance = Products.objects.get(name=name)
        #     if product_instance is not None:
        #         instance.products.add(product_instance)
        # instance.save()

class CartSerializer(ModelSerializer):
    user = CharField()
    products = ProductsSerializer(many=True,read_only=True)

    # def get_products(self,obj):
    #     product_queryset = obj.products.all()
    #     print(product_queryset)
    #     print("Reached here")
    #     serialized_products = CartProductsCreationSerializer(product_queryset,many=True,read_only=True).data
    #     print(serialized_products)
    #     return serialized_products
    

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.pop('user',None)
        user = User.objects.get(username=username)
        # instance = self.Meta.model(**validated_data)
        
        if user is None:
            raise APIException("User does not exist")
        instance = self.Meta.model(**validated_data)
        instance.user = user
        instance.save()
        return instance
# class CartSerializer(ModelSerializer):
#     products = ProductsSerializer()

#     class Meta:
#         model = Cart