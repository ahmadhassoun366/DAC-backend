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
    path('management/add', ManagementCreateAPIView.as_view(), name='addManagement'),
    path('management/<int:management_id>/update', ManagementUpdateAPIView.as_view(), name='updateManagement'),
    path('management/<int:management_id>/delete', ManagementDeleteAPIView.as_view(), name='deleteManagement'),
    
    path('accounting/<int:company_id>/', AccountingViewSet.as_view(), name='accounting'),
    path('accounting/add', AccountingCreateAPIView.as_view(), name='addAccounting'),
    path('accounting/<int:accounting_id>/update', AccountingUpdateAPIView.as_view(), name='updateAccounting'),
    path('accounting/<int:accounting_id>/delete', AccountingDeleteAPIView.as_view(), name='deleteAccounting'),

    path('unit/', UnitViewSet.as_view(), name='unit'),
    path('unit/add', UnitCreateAPIView.as_view(), name='addUnit'),
    path('unit/<int:unit_id>/update', UnitUpdateAPIView.as_view(), name='updateUnit'),
    path('unit/<int:unit_id>/delete', UnitDeleteAPIView.as_view(), name='deleteUnit'),
    path('unit/<int:unit_id>/', UnitIdViewSet.as_view(), name='unitId'),

    path('subunit/', SubUnitViewSet.as_view(), name='subunit'),
    path('subunit/add', SubUnitCreateAPIView.as_view(), name='addSubUnit'),
    path('subunit/<int:subunit_id>/update', SubUnitUpdateAPIView.as_view(), name='updateSubUnit'),
    path('subunit/<int:subunit_id>/delete', SubUnitDeleteAPIView.as_view(), name='deleteSubUnit'),
    path('subunit/<int:subunit_id>/', SubUnitIdViewSet.as_view(), name='subunitId'),


]