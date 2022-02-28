from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    is_user = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_technical = models.BooleanField(default=False)
    username = models.EmailField(unique=True)
    name = models.CharField(max_length=256)
    gender = models.CharField(max_length=24)
    phone_number = models.BigIntegerField(null=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    phr_address = models.CharField(max_length=20, blank=True, null=True)

class HealthCard(models.Model):
    card = models.ImageField(upload_to='media/health_world/cards/',blank=False)