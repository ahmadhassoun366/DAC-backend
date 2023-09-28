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

# use it with POST request
class PostCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


# use it with GET request
class GetCompanySerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"

class GetAccoutingSerializer(serializers.ModelSerializer):
    company = GetCompanySerializer(read_only=True)
    manager = ManagerSerializer(read_only=True)
    class Meta:
        model = Accounting
        fields = "__all__"

class GetManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = "__all__"


class PostManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = "__all__"

class PostAccountingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounting
        fields = "__all__"

class ItemSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)
    Tva = GetManagementSerializer(read_only=True)
    class Meta:
        model = Item
        fields = "__all__"

class PostItemSerializer(serializers.ModelSerializer):
    Tva = GetManagementSerializer()
    class Meta:
        model = Item
        fields = "__all__"

class ItemIdSerializer(serializers.ModelSerializer):
    company = GetCompanySerializer(read_only=True)
    Management = GetManagementSerializer(read_only=True)
    Accounting = GetAccoutingSerializer(read_only=True)
    class Meta:
        model = Item
        fields = "__all__"

class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class ItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class SubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"

class UnitSerializer(serializers.ModelSerializer):
    sub_unit = SubUnitSerializer(read_only=True)
    class Meta:
        model = Unit
        fields = "__all__"


class GetSubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"

class GetSubUnitIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"

class UnitIdSerializer(serializers.ModelSerializer):
    sub_unit = GetSubUnitIdSerializer(read_only=True)
    class Meta:
        model = Unit
        fields = "__all__"

class GetUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class PostUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class UnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class UnitDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class PostSubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"

class SubUnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"

class SubUnitDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = "__all__"
