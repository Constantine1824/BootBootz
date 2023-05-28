from rest_framework.serializers import ModelSerializer,CharField
from .models import Order
from Auth.models import User
from Core.models import Address,Boots,Variants
from rest_framework.exceptions import APIException,ValidationError,ParseError
from rest_framework import serializers


class OrderSerializer(ModelSerializer):

    class Meta:
             model = Order
             fields = '__all__'


class OrderCreationSerializer(serializers.Serializer):
    tracking_id = serializers.CharField(read_only=True)
    user = serializers.CharField()
    order_summary = serializers.JSONField()

    def check_validate(self,data):
            # First we check for the validity of the user
        boot_obj : Boots
        variant : BootsVariants
        username = data['user']
        user = User.objects.get(username=username)
        if user is None:
            raise ValidationError({
            "detail" : "User does not exist"
                })
            # We check if the products are present in the order summary
        products = data['order_summary']['boots']
        total_price = 0
        for dicts in products:
            name,price,color,quantity = dicts['name'],dicts['price'],dicts['color'],dicts['quantity']
            #First check if the product exist using the name
            try:
                boot_obj = Boots.objects.get(name=name)
            except Boots.DoesNotExist:
                #if boot_obj is None:
                raise ValidationError({
                        'detail' : 'The boot objects does not exist in the database'
                     }) 
            else: 
            # Check if the price is equal
            # Cast to string since the expected value is a string
                if f'{boot_obj.price}' != price:
                    raise ValidationError({
                        'detail' : 'Price is not equal'
                        }) 
                else:
                    # Check the color and quantity if its available or not
                    try:
                        variant = BootsVariants.objects.get(boot=boot_obj,color=color)
                    except BootsVariants.DoesNotExist:
                        raise ValidationError({
                                'detail' : 'This product is not available'
                            })
                    else:
                        if variant.quantity_available < quantity:
                            raise ParseError('Quantity greater than quantity available')
                        variant.quantity_available = variant.quantity_available - quantity
                        variant.save()
                        total_price += price
        return True
                
    
    def create(self, validated_data):
        if self.check_validate(validated_data):
            username = validated_data.pop('user',None)
            user = User.objects.get(username=username)
            delivery_address = Address.objects.get(user=user)
            if delivery_address is None:
                raise ParseError()
            return Order.objects.create(user=user,order_summary=validated_data['order_summary'],\
                                         delivery_address=delivery_address,status='PEN')     