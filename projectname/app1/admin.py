from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *
# Register your models here.
class EmailUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'company','address','city','country')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'manager', 'brand','taxIdentification','commercialRegister','phone','Address')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('code','name','unit','quantity')

class AccountingAdmin(admin.ModelAdmin):
    list_display = ('revenue','purchase','expense','change_inv_acc')

class ManagementAdmin(admin.ModelAdmin):
    list_display = ('TVA',)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name','unit_symbol','sub_unit')

class SubUnitAdmin(admin.ModelAdmin):
    list_display = ('name','sub_unit_symbol')

admin.site.register(CustomUser, EmailUserAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Accounting, AccountingAdmin)
admin.site.register(Management, ManagementAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(SubUnit, SubUnitAdmin)