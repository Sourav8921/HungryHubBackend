from rest_framework import serializers
from .models import CustomUser, DeliveryAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Method to create a new user instance
        # Extract validated data and use it to create a new user
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        # Set the password for the user using the hashed password from validated data
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
