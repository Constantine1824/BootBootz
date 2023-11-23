from rest_framework.serializers import ModelSerializer,CharField
from .models import Boots,Address,Reviews, Variants
from Auth.models import User
from Auth.serializers import UserSerializer
from Admin.serializers import VariantsSerializer

class AddressCreationSerializer(ModelSerializer):
    """This serializer creates an address object"""
    user = CharField()
    
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        print(self.initial_data)
        username = validated_data.pop('user',None)
        user_obj = User.objects.get(username=username)
        instance = self.Meta.model(**validated_data)
        instance.user = user_obj
        instance.save()
        return instance



class VariantSerializer(ModelSerializer):
    class Meta:
        model = Variants
        fields = ['id','quantity_available', 'color', 'image_1', 'image_2', 'image_3']

class BootsSerializer(ModelSerializer):
    class Meta:
        model = Boots
        fields = '__all__'

class BootsDetailsSerializer(ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    class Meta:
        model = Boots
        fields = ['id','name', 'price', 'manufacturer', 'default_img', 'category', 'rating', 'availability_status', 'variants']

class ReviewsSerializer(ModelSerializer):

    user = UserSerializer(read_only = True)
    product = CharField()

    def __init__(self, instance=None, data=...,user=None, **kwargs):
        self.user = user
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Reviews
        fields = '__all__'

    def save(self,validated_data):
        product_name = validated_data.pop('product',None)
        boots_obj = Boots.objects.get(product_name)
        instance = self.Meta.model(**validated_data)
        instance.product = boots_obj
        instance.user = self.user
        instance.save()
        return instance