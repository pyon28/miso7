from django.db import models
from django.utils import timezone
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

class Item(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)  
    name = models.CharField(verbose_name='商品名', max_length=40)
    image = models.ImageField(verbose_name='画像', upload_to='item_images/', blank=True, null=True)  
    used_miso = models.BooleanField(verbose_name='使った味噌', default=False)
    thoughts = models.TextField(verbose_name='メモ・感想', null=True, blank=True)
    taste_rating = models.IntegerField(verbose_name='味', choices=[(1, '1'), (2, '2'), (3, '3')], null=True, blank=True)
    appearance_rating = models.IntegerField(verbose_name='見た目', choices=[(1, '1'), (2, '2'), (3, '3')], null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='編集日時', blank=True, null=True)
   

    def __str__(self):
        return self.name
    

