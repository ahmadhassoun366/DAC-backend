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