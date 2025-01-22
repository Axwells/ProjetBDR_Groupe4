from rest_framework import serializers
from .models import Brand, Car, AppUser, Image, Brake, Engine, Transmission, Performance, Category, Specification, Specification_Engine, Category_Specification
from django.contrib.auth import authenticate

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = AppUser
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return AppUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        return user

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'modelNameCar']

class CarSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['modelName', 'numberOfSeats', 'releaseDate', 'defaultPrice', 'nameBrand', 'images']
