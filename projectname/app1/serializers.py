from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class GETUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'phone', 'email')

class POSTUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create(password=make_password(password), **validated_data)
        return user

    


class ManagerSerializer(serializers.ModelSerializer):
    user = GETUserSerializer(read_only=True)


    class Meta:
        model = Manager
        fields = "__all__"


class PostManagerSerializer(serializers.ModelSerializer):
    # user = GETUserSerializer(read_only=True)
    # country = CountrySerializer(read_only=True)  # Use the nested serializer for country field

    class Meta:
        model = Manager
        fields = "__all__"
