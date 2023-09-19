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

    path('item/add', ItemCreateAPIView.as_view(), name='addItem'),
    path('item/<int:manager_id>/', ItemViewSet.as_view(), name='Item'),
    path('item/details/<int:item_id>/', ItemIdViewSet.as_view(), name='Item'),
    path('item/<int:item_id>/update', ItemUpdateAPIView.as_view(), name='updateItem'),
    path('item/<int:item_id>/delete', Delete.as_view(), name='deleteItem'),
    
    path('management/<int:company_id>/', ManagementViewSet.as_view(), name='management'),
    path('accounting/<int:company_id>/', AccountingViewSet.as_view(), name='accounting'),


]