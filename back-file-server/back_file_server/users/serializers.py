from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[validate_password]
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:

        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'token']

    def create(self, validated_data):
        return CustomUser.objects.create_user(username=validated_data["username"], password=validated_data["password"], phone_number=validated_data["phone_number"])

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

