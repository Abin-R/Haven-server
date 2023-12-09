from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    online = models.BooleanField(default = False)  
    address = models.CharField(max_length=255, null=True, blank=True) 
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)