from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, unique=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name="Users Image")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name','phone_number']

    def __str__(self):
        return f"{self.full_name} - {self.email}"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='regular_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.full_name