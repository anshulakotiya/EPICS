from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    username = models.EmailField(unique=True)
    name = models.CharField(max_length=256)
    gender = models.CharField(max_length=24)
    mobile_number = models.BigIntegerField()
    card_number = models.CharField(max_length=20)
