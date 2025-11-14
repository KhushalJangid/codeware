from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email=None,password=None,**extra):
        if not email:
            raise ValueError('Email  is required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        extra.setdefault('is_active',True)

        if extra.get('is_staff') is not True:
            raise ValueError(('is_staff should be True for Superuser'))

        return self.create_user(password=password,**extra) 
    

class User(AbstractUser):
    username = None
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(blank=True,null=True,unique=True)
    objects = UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
