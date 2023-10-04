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
    
    path('tva/', TVAViewSet.as_view(), name='tva'),
    path('tva/add', TVACreateAPIView.as_view(), name='addTVA'),
    path('tva/<int:tva_id>/update', TVAUpdateAPIView.as_view(), name='updateTVA'),
    path('tva/<int:tva_id>/delete', TVADeleteAPIView.as_view(), name='deleteTVA'),
    path('tva/<int:tva_id>/', TVAIdViewSet.as_view(), name='tvaId'),
    
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

    path('revenue/add', RevenueCreateAPIView.as_view(), name='addRevenue'),
    path('revenue/<int:revenue_id>/update', RevenueUpdateAPIView.as_view(), name='updateRevenue'),
    path('revenue/<int:revenue_id>/delete', RevenueDeleteAPIView.as_view(), name='deleteRevenue'),
    path('revenue/<int:revenue_id>/', RevenueIdViewSet.as_view(), name='revenueId'),

    path('expense/add', ExpenseCreateAPIView.as_view(), name='addExpense'),
    path('expense/<int:expense_id>/update', ExpenseUpdateAPIView.as_view(), name='updateExpense'),
    path('expense/<int:expense_id>/delete', ExpenseDeleteAPIView.as_view(), name='deleteExpense'),
    path('expense/<int:expense_id>/', ExpenseIdViewSet.as_view(), name='expenseId'),

    path('purchase/add', PurchaseCreateAPIView.as_view(), name='addPurchase'),
    path('purchase/<int:purchase_id>/update', PurchaseUpdateAPIView.as_view(), name='updatePurchase'),
    path('purchase/<int:purchase_id>/delete', PurchaseDeleteAPIView.as_view(), name='deletePurchase'),
    path('purchase/<int:purchase_id>/', PurchaseIdViewSet.as_view(), name='purchaseId'),

    path('changeinvacc/add', ChangeInvAccCreateAPIView.as_view(), name='addChangeInvAcc'),
    path('changeinvacc/<int:changeinvacc_id>/update', ChangeInvAccUpdateAPIView.as_view(), name='updateChangeInvAcc'),
    path('changeinvacc/<int:changeinvacc_id>/delete', ChangeInvAccDeleteAPIView.as_view(), name='deleteChangeInvAcc'),
    path('changeinvacc/<int:changeinvacc_id>/', ChangeInvAccIdViewSet.as_view(), name='changeinvaccId'),    
]