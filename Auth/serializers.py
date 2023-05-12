from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework.exceptions import APIException

class UserCreationSerializer(ModelSerializer):
    

    class Meta:
        model = User
        fields = ['username', 'password','email','first_name', 'last_name','is_verified']

        extra_kwargs = {
            'password': {
                'write_only' : True
            },
            'is_verified' : {
                'read_only' : True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        else:
            raise APIException('Password is incorrect')
        return instance
    
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'is_verified']