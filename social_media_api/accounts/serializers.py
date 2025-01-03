from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Get the custom user model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data.get('email'), password=validated_data['password'], bio=validated_data.get('bio', ''), profile_picture=validated_data.get('profile_picture', None),)
        Token.objects.create(user=user)
        return user
