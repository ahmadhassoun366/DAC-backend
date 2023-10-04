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
from django.http import QueryDict

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
        itemData = request.data.copy() if isinstance(request.data, QueryDict) else dict(request.data)
        
        if 'image' in request.FILES:
            itemData['image'] = request.FILES['image']

        print(itemData)

        itemData.update({
            'manager': itemData.get('manager'),
            'supcode': itemData.get('supcode'),
            'code': itemData.get('code'),
            'name': itemData.get('name'),
            'unit': itemData.get('unit'),
            'quantity': itemData.get('quantity'),
            'total': itemData.get('total'),
            'tva': itemData.get('tva'),
            'ttc': itemData.get('ttc'),
            'place': itemData.get('place'),
            'addValueCost': itemData.get('addValueCost'),
            'cost': itemData.get('cost'),
            'revenue': itemData.get('revenue'),
            'purchase': itemData.get('purchase'),
            'expense': itemData.get('expense'),
            'final_good': itemData.get('final_good'),
            'change_inv_acc': itemData.get('change_inv_acc'),
            'image': itemData.get('image'),
            'minimum_quantity': itemData.get('minimum_quantity'),
            'kind': itemData.get('kind'),
        })
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
        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class Delete(APIView):
    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ManagementViewSet(APIView):
    def get(self, request, company_id):
        management = Management.objects.filter(company=company_id)
        serializer = GetManagementSerializer(management, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AccountingViewSet(APIView):
    def get(self, request, company_id):
        accounting = Accounting.objects.filter(company=company_id)
        serializer = GetAccoutingSerializer(accounting, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnitViewSet(APIView):
    def get(self, request):
        unit = Unit.objects.all()
        serializer = UnitSerializer(unit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnitIdViewSet(APIView):
    def get(self, request, unit_id):
        unit = Unit.objects.filter(id=unit_id).first()
        if not unit:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnitSerializer(unit)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnitCreateAPIView(APIView):
    def post(self, request):
        serializer = PostUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class UnitUpdateAPIView(APIView):
    def put(self, request, unit_id):
        try:
            unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostUnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class UnitDeleteAPIView(APIView):
    def delete(self, request, unit_id):
        try:
            unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubUnitViewSet(APIView):
    def get(self, request):
        subunit = SubUnit.objects.all()
        serializer = SubUnitSerializer(subunit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class SubUnitIdViewSet(APIView):
    def get(self, request, subunit_id):
        subunit = SubUnit.objects.filter(id=subunit_id).first()
        if not subunit:
            return Response({"error": "SubUnit not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetSubUnitSerializer(subunit)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubUnitCreateAPIView(APIView):
    def post(self, request):
        serializer = PostSubUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class SubUnitUpdateAPIView(APIView):
    def put(self, request, subunit_id):
        try:
            subunit = SubUnit.objects.get(id=subunit_id)
        except ObjectDoesNotExist:
            return Response({"error": "SubUnit not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSubUnitSerializer(subunit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class SubUnitDeleteAPIView(APIView):
    def delete(self, request, subunit_id):
        try:
            subunit = SubUnit.objects.get(id=subunit_id)
        except ObjectDoesNotExist:
            return Response({"error": "SubUnit not found"}, status=status.HTTP_404_NOT_FOUND)

        subunit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TVAViewSet(APIView):
    def get(self, request):
        tva = TVA.objects.all()
        serializer = GetTVASerializer(tva, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TVAIdViewSet(APIView):
    def get(self, request, tva_id):
        tva = TVA.objects.filter(id=tva_id).first()
        if not tva:
            return Response({"error": "TVA not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetTVASerializer(tva)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TVACreateAPIView(APIView):
    def post(self, request):
        serializer = PostTVASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class TVAUpdateAPIView(APIView):
    def put(self, request, tva_id):
        try:
            tva = TVA.objects.get(id=tva_id)
        except ObjectDoesNotExist:
            return Response({"error": "TVA not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostTVASerializer(tva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class TVADeleteAPIView(APIView):
    def delete(self, request, tva_id):
        try:
            tva = TVA.objects.get(id=tva_id)
        except ObjectDoesNotExist:
            return Response({"error": "TVA not found"}, status=status.HTTP_404_NOT_FOUND)

        tva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ~~~~~~~~~~~~~~~~~~~~~~ Purchase Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   


class RevenueIdViewSet(APIView):
    def get(self, request, revenue_id):
        revenue = Revenue.objects.filter(id=revenue_id).first()
        if not revenue:
            return Response({"error": "Revenue not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetRevenueSerializer(revenue)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RevenueCreateAPIView(APIView):
    def post(self, request):
        serializer = PostRevenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class RevenueUpdateAPIView(APIView):
    def put(self, request, revenue_id):
        try:
            revenue = Revenue.objects.get(id=revenue_id)
        except ObjectDoesNotExist:
            return Response({"error": "Revenue not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostRevenueSerializer(revenue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class RevenueDeleteAPIView(APIView):
    def delete(self, request, revenue_id):
        try:
            revenue = Revenue.objects.get(id=revenue_id)
        except ObjectDoesNotExist:
            return Response({"error": "Revenue not found"}, status=status.HTTP_404_NOT_FOUND)

        revenue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ~~~~~~~~~~~~~~~~~~~~~~ Expense Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   


class ExpenseIdViewSet(APIView):
    def get(self, request, expense_id):
        expense = Expense.objects.filter(id=expense_id).first()
        if not expense:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseCreateAPIView(APIView):
    def post(self, request):
        serializer = PostExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseUpdateAPIView(APIView):
    def put(self, request, expense_id):
        try:
            expense = Expense.objects.get(id=expense_id)
        except ObjectDoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDeleteAPIView(APIView):
    def delete(self, request, expense_id):
        try:
            expense = Expense.objects.get(id=expense_id)
        except ObjectDoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ~~~~~~~~~~~~~~~~~~~~~~ Purchase Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   


class PurchaseIdViewSet(APIView):
    def get(self, request, purchase_id):
        purchase = Purchase.objects.filter(id=purchase_id).first()
        if not purchase:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetPurchaseSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PurchaseCreateAPIView(APIView):
    def post(self, request):
        serializer = PostPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseUpdateAPIView(APIView):
    def put(self, request, purchase_id):
        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except ObjectDoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostPurchaseSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseDeleteAPIView(APIView):
    def delete(self, request, purchase_id):
        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except ObjectDoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeInvAccIdViewSet(APIView):
    def get(self, request, change_inv_acc_id):
        change_inv_acc = ChangeInvAcc.objects.filter(id=change_inv_acc_id).first()
        if not change_inv_acc:
            return Response({"error": "ChangeInvAcc not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetChangeInvAccSerializer(change_inv_acc)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class ChangeInvAccCreateAPIView(APIView):
    def post(self, request):
        serializer = PostChangeInvAccSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class ChangeInvAccUpdateAPIView(APIView):
    def put(self, request, change_inv_acc_id):
        try:
            change_inv_acc = ChangeInvAcc.objects.get(id=change_inv_acc_id)
        except ObjectDoesNotExist:
            return Response({"error": "ChangeInvAcc not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostChangeInvAccSerializer(change_inv_acc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class ChangeInvAccDeleteAPIView(APIView):
    def delete(self, request, change_inv_acc_id):
        try:
            change_inv_acc = ChangeInvAcc.objects.get(id=change_inv_acc_id)
        except ObjectDoesNotExist:
            return Response({"error": "ChangeInvAcc not found"}, status=status.HTTP_404_NOT_FOUND)

        change_inv_acc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

