from django.contrib.auth import get_user_model
from rest_framework import serializers

# Get the custom user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # CharField for password with write-only property

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is not returned in the response
        }

    def create(self, validated_data):
        """
        Create a new user instance using the provided validated data.
        """
        # Use the custom `create_user` method of the user model
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user