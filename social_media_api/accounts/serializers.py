from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Get the custom user model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['id','username', 'email', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        user = get_user_model.objects.create_user()
        Token.objects.create(user=user)
        return user
