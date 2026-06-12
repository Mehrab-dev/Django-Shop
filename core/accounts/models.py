from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class UserType(models.IntegerChoices):
    customer = 1
    admin = 2
    superuser = 3 


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("the email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("type", UserType.superuser.value)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("type") is not UserType.superuser.value:
            raise ValueError("super user must have type = superuser")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("super user must have is_staff = True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("super user must have is_active = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("super user must have is_superuser = True")
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    type = models.IntegerField(choices=UserType.choices,default=UserType.customer.value)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    phone_number = models.CharField(blank=True)
    image = models.ImageField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.customer.value:
        CustomerProfile.objects.create(user=instance, pk=instance.pk)