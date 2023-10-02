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


class TVA (models.Model):
    class Meta:
        verbose_name = "TVA"
        verbose_name_plural = "TVAs"
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='managements')
    value = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.value}"

class Revenue(models.Model):
    value = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='revnues')
    def __str__(self):
        return f"{self.value}"

class Purchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='purchases')
    value = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.value}"

class Expense(models.Model):
    value = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f"{self.value}"

class ChangeInvAcc(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='change_inv_acc')
    value = models.BooleanField(null=True, blank=True)
    def __str__(self):
        return f"{self.value}"


class Item(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    FINAL_GOOD_CHOICES = [
        ('start', 'Start'),
        ('mid', 'Mid'),
        ('finish', 'Finished'),
    ]   

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='items')
    supcode = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)   
    tva = models.ForeignKey(TVA, on_delete=models.SET_NULL, null=True, blank=True)
    ttc = models.FloatField(null=True, blank=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    addValueCost = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    revenue = models.ForeignKey(Revenue, related_name='revenue_item', on_delete=models.SET_NULL, null=True, blank=True)
    purchase = models.ForeignKey(Purchase, related_name='purchase_item', on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(Expense, related_name='expense_item', on_delete=models.SET_NULL, null=True, blank=True)
    final_good = models.CharField(max_length=10, choices=FINAL_GOOD_CHOICES, default='finished', null=True, blank=True)
    change_inv_acc = models.ForeignKey(ChangeInvAcc, related_name='change_inv_acc_item', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='static/item_images', null=True, blank=True)
    minimum_quantity = models.IntegerField(null=True, blank=True)
    kind = models.CharField(max_length=200, null=True, blank=True)
    
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

class ManagementItem(models.Model):
    Tva = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.management} - {self.item}"

class SubUnit (models.Model):
    class Meta:
        verbose_name = "SubUnit"
        verbose_name_plural = "SubUnits"
    name = models.CharField(max_length=200, null=True, blank=True)
    sub_unit_symbol = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class Unit (models.Model):
    OPERATION = [
        ('*', 'Multiplication'),
        ('/', 'Division'),
        ('+', 'Addition'),
        ('-', 'Substraction'),
    ]

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    operation = models.CharField(max_length=1, choices=OPERATION, null=True, blank=True)
    unit_symbol = models.CharField(max_length=200, null=True, blank=True)
    sub_unit = models.ForeignKey(SubUnit, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"




   