from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token

# Get the custom user model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'bio', 'profile_picture', 'followers']

        