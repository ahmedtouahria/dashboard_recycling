from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')
        if not name:
            raise ValueError('user must have a name')
        user_obj = self.model(
            name=name,
            phone=phone,
            password=password
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, name, phone, password=None):
        user = self.create_user(
            name,
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, name, phone, password=None):
        user = self.create_user(
            name,
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=20, blank=False,
                            null=False, unique=True)
    password = models.CharField(
        max_length=100, blank=False, null=False, validators=[MinLengthValidator(8)])
    is_deche_vendeur = models.BooleanField(default=False)
    is_mp_client = models.BooleanField(default=False)
    address=models.CharField(max_length=120,null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    created_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name
    def get_full_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Product(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=120)
    quantity=models.IntegerField(default=0)
    price=models.FloatField(default=0.0)
    photo=models.ImageField(upload_to="media/product")
    @property
    def get_total(self):
        return self.price*self.quantity
    
    def __str__(self):
        return self.name

class MatierPremier(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=120)
    quantity=models.IntegerField(default=0)
    price=models.FloatField(default=0.0)
    photo=models.ImageField(upload_to="media/mp")
    
    @property
    def get_total(self):
        return self.price*self.quantity
    def __str__(self):
        return self.name

class Contrat(models.Model):
    enterprise=models.ForeignKey(Customer,on_delete=models.CASCADE)
    matier=models.ForeignKey(MatierPremier,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    total_price=models.FloatField(default=0.0)
    date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)