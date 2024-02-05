from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')

class Items(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)  
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/')
    used_miso = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.name
    
class UsedMisoList(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.timestamp}"
    
class UsedMisoDetail(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='used_miso_details')
    thoughts = models.TextField(null=True, blank=True)
    taste_rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], null=True, blank=True)
    appearance_rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.timestamp}"