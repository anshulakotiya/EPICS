from django.contrib.auth.models import AbstractUser
from django.db import models


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
    card = models.ImageField(upload_to='media/health_world/cards/', blank=False)


class doctorLicence(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    licence_no = models.CharField(max_length=64)
    licence_image = models.ImageField(upload_to='media/health_world/licence/', blank=False)


class UserDecease(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decease_name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)

class Documents(models.Model):
    userDoc = models.ForeignKey(UserDecease,on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/health_world/documents/', blank=False)

