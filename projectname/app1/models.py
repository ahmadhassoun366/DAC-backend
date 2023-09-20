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

class Management(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='managements')
    TVA = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.TVA}"

class Accounting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='accountings')
    revenue = models.FloatField(null=True, blank=True)
    purchase = models.FloatField(null=True, blank=True)
    expense = models.FloatField(null=True, blank=True)
    change_inv_acc = models.BooleanField(default=False)
    def __str__(self):
        return f"Accounting object for company {self.company.name} with Revenue: {self.revenue}, Purchase: {self.purchase}, Expense: {self.expense}, Change in Inv Acc: {self.change_inv_acc}"
        
class Item(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    FINAL_GOOD_CHOICES = [
        ('start', 'Start'),
        ('mid', 'Mid'),
        ('finish', 'Finished'),
    ]   

    TVA = [
        (0, '0%'),
        (0.05, '5%'),
        (0.1, '10%'),
    ]
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='items')
    supcode = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)   
    # TVA = models.ForeignKey(Management, on_delete=models.SET_NULL, null=True, blank=True)
    ttc = models.FloatField(null=True, blank=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    addValueCost = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    # revenue = models.ForeignKey(Accounting, related_name='revenue_item', on_delete=models.SET_NULL, null=True, blank=True)
    # purchase = models.ForeignKey(Accounting, related_name='purchase_item', on_delete=models.SET_NULL, null=True, blank=True)
    # expense = models.ForeignKey(Accounting, related_name='expense_item', on_delete=models.SET_NULL, null=True, blank=True)
    final_good = models.CharField(max_length=10, choices=FINAL_GOOD_CHOICES, default='finished', null=True, blank=True)
    # change_inv_acc = models.ForeignKey(Accounting, related_name='change_inv_acc_item', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='static/item_images', null=True, blank=True)
    minimum_quantity = models.IntegerField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    purchase = models.FloatField(null=True, blank=True)
    expense = models.FloatField(null=True, blank=True)
    change_inv_acc = models.BooleanField(default=False)
    tva = models.FloatField(choices=TVA, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # If you have all the necessary fields to calculate 'total', then do so
        if self.quantity is not None and self.price is not None:
            self.total = self.quantity * self.price

        # Only calculate cost if both addValueCost and price are available
        if self.addValueCost is not None and self.price is not None:
            self.cost = self.addValueCost + self.price

        # Only calculate ttc if both cost and tva are available
        if self.cost is not None and self.tva is not None:
            self.ttc = self.cost * (1 + self.tva)  # Assuming that 'tva' is in decimal form like 0.2 for 20%

        super(Item, self).save(*args, **kwargs)


class Unite (models.Model):
    class Meta:
        verbose_name = "Unite"
        verbose_name_plural = "Unites"
    name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

   