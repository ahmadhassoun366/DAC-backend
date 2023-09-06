from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from datetime import datetime
from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

class ManagerRegisterCreateAPIView(APIView):
    def post(self, request):
        serializerUser = POSTUserSerializer(data=request.data)
        if serializerUser.is_valid():
            user = serializerUser.save()
            # deactivating the user until he verifies his account
            user.save()

            # Create a Seeker instance and associate it with the newly created user
            manager_data = {
                'user': user.id,
            }
            manager_serializer = PostManagerSerializer(data=manager_data)
            if manager_serializer.is_valid():
                manager_serializer.save()
            else:
                # If seeker serializer is invalid, delete the user as well
                user.delete()
                return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializerUser.data, status=status.HTTP_201_CREATED)
        return Response(serializerUser.errors, status=status.HTTP_400_BAD_REQUEST)

# @permission_classes([IsAuthenticated])
class ManagerViewSet(APIView):
    def get(self, request, user_id):
        # Logic for handling GET request
        manager = Manager.objects.filter(user=user_id)  
        serializer = ManagerSerializer (manager, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

# @permission_classes([IsAuthenticated])
class CompanyRegisterCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        companyData = {
            'manager': data.get('manager'),
            'brand': data.get('brand'),
            'name': data.get('name'),
            'logo': data.get('logo'),
            'taxIdentification': data.get('taxIdentification'),
            'commercialRegister': data.get('commercialRegister'),
            'phone': data.get('phone'),
            'Address': data.get('Address'),
        }
        print(companyData)

        serializer = PostCompanySerializer(data=companyData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @permission_classes([IsAuthenticated])
class CompanyViewSet(APIView):
    def get(self, request, manager_id): 
        company = Company.objects.filter(manager=manager_id)
        serializer = GetCompanySerializer(company, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @permission_classes([IsAuthenticated])
class ItemCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        itemData = {
            'manager': data.get('manager'),
            'supcode': data.get('supcode'),
            'code': data.get('code'),
            'name': data.get('name'),
            'unit': data.get('unit'),
            'quantity': data.get('quantity'),
            'total': data.get('total'),
            'TVA': data.get('TVA'),
            'TVA_value': data.get('TVA_value'),
            'TTC': data.get('TTC'),
            'place': data.get('place'),
            'addValueCost': data.get('addValueCost'),
            'unit_price': data.get('unit_price'),
            'cost': data.get('cost'),
            'revenue': data.get('revenue'),
            'purchase': data.get('purchase'),
            'expense': data.get('expense'),
            'final_good': data.get('final_good'),
            'change_inv_acc': data.get('change_inv_acc'),
            'inventory_acc': data.get('inventory_acc'),
            # 'image': data.get('image')  # You'll likely handle this separately
        }
        print(itemData)

        serializer = PostItemSerializer(data=itemData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemIdViewSet(APIView):
    def get(self, request, item_id):
        item = Item.objects.filter(id=item_id)
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemViewSet(APIView):
    def get(self, request, manager_id):
        item = Item.objects.filter(manager=manager_id)
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemUpdateAPIView(APIView):
    def put(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = PostItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ItemDeleteAPIView(APIView):
    def delete(self, request, item_id):
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)