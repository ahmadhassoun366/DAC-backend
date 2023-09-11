from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Manager(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True, blank=True)
    company = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    def __str__(self):
        return f"{self.user}"




class Company(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
    logo = models.ImageField(upload_to='static/company_images', null=True, blank=True)
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='companies')
    brand = models.CharField(max_length=200, null=True, blank=True)
    taxIdentification = models.CharField(max_length=20, null=True, blank=True)
    commercialRegister = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class TVA(models.Model):
    class Meta:
        verbose_name = "TVA"
        verbose_name_plural = "TVAs"

    name = models.CharField(max_length=100)
    rate = models.FloatField()  # Store it as percentage e.g. 18.0 for 18%

    def __str__(self):
        return f"{self.name} ({self.rate}%)"

class Item(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='items')
    supcode = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)   
    TVA = models.ForeignKey(TVA, on_delete=models.SET_NULL, null=True, blank=True)
    TVA_value = models.FloatField(null=True, blank=True) 
    TTC = models.FloatField(null=True, blank=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    addValueCost = models.FloatField(null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    purchase = models.FloatField(null=True, blank=True)
    expense = models.FloatField(null=True, blank=True)
    final_good = models.BooleanField(default=True)
    change_inv_acc = models.BooleanField(default=False)
    inventory_acc = models.CharField(max_length=20, choices=[('A', 'Inventory Account A'), ('B', 'Inventory Account B')], null=True, blank=True , default='A')
    image = models.ImageField(upload_to='static/item_images', null=True, blank=True)

    def calculate_total(self):
        if self.quantity and self.unit_price:
            self.total = self.quantity * self.unit_price
        else:
            self.total = None

    def calculate_TTC(self):
        if self.TVA and self.total:
            self.TTC = self.total + self.TVA_value
        else:
            self.TTC = None

    def calculate_cost(self):
        if self.quantity and self.unit_price:
            self.cost = self.quantity * self.unit_price + self.addValueCost
        else:
            self.cost = None

    def calculate_revenue(self):
        if self.quantity and self.unit_price:
            self.revenue = self.quantity * self.unit_price
        else:
            self.revenue = None

    def calculate_profit(self):
        if self.revenue and self.cost:
            self.profit = self.revenue - self.cost
        else:
            self.profit = None

