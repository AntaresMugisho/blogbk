# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from utils import random_filename


class Role(models.Model):
    class RoleChoices(models.TextChoices):
        SUPERADMIN = "SU", _("Super Administrator")
        ADMIN = "AD", _("Administrator")

    name = models.CharField(max_length=2, choices=RoleChoices.choices)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to=random_filename, null=True, blank=True)
    roles = models.ManyToManyField(Role, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Blacklisted token from {self.blacklisted_at}"

