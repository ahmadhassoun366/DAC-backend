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

class TVAAdmin(admin.ModelAdmin):
    list_display = ('name','rate')

admin.site.register(CustomUser, EmailUserAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(TVA, TVAAdmin)
