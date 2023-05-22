from Core.models import Boots,Variants
from rest_framework import serializers

class VariantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variants
        fields = '__all__'


class BootsCreationSerializer(serializers.ModelSerializer):

    variants = VariantsSerializer(many=True)

    class Meta:
        model = Boots
        fields = '__all__'
        extra_kwargs = {
            'date_added' : {
                'read_only' : True
            },
            'slug' : {
                'read_only' : True
            },
            'rating' : {
                'read_only' : True
            }
        }