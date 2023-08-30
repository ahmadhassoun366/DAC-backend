from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from .views import *

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('manager/register', ManagerRegisterCreateAPIView.as_view(), name='Manager_register'),
    path('manager/<int:user_id>/', ManagerViewSet.as_view(), name='manager'),

    path('company/<int:manager_id>/', CompanyViewSet.as_view(), name='manager_company'),
    path('company_register/', CompanyRegisterCreateAPIView.as_view(), name='company_register'),
]