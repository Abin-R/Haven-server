from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import serializers
from .models import CustomUser
from .utils import *


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Customize the token payload here
        token['username'] = user.username
        # Add more claims if needed
        token['role'] = get_user_role(user) 

        return token

class UserSerializers(serializers.ModelSerializer): 
    class Meta:
        model = CustomUser
        fields = ['id','username','email','password', 'phone', 'image', 'online']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    