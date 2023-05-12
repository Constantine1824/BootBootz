from rest_framework.serializers import ModelSerializer,CharField
from .models import Boots,Address,Reviews,BootsVariants,Size
from Auth.models import User

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
        
class SizeSerializer(ModelSerializer):

    class Meta:
        model = Size
        fields = ['size']

class BootsSerializer(ModelSerializer):
    
    size = SizeSerializer(many=True)

    class Meta:
        model = Boots
        fields = '__all__'

class BootsVariantsSerializer(ModelSerializer):
    boot = BootsSerializer()

    class Meta:
        model = BootsVariants
        fields = '__all__'

class ReviewsSerializer(ModelSerializer):

    user = CharField(read_only = True)
    product = CharField()

    class Meta:
        model = Reviews
        fields = '__all__'

    def save(self,validated_data):
        user = self.context['request'].user
        product_name = validated_data.pop('product',None)
        boots_obj = Boots.objects.get(product_name)
        instance = self.Meta.model(**validated_data)
        instance.product = boots_obj
        instance.user = user
        instance.save()
        return instance