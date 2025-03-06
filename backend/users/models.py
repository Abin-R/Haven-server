from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class CustomUser(AbstractUser):
    NORMAL = 'normal'
    SUPER_USER = 'super_user'
    PREMIUM = 'premium'

    SUBSCRIPTION_CHOICES = [
        (NORMAL, 'Normal User'),
        (SUPER_USER, 'Super User'),
        (PREMIUM, 'Premium User'),
    ]
    phone = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    online = models.BooleanField(default = False)  
    address = models.CharField(max_length=255, null=True, blank=True) 
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default=NORMAL)
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    def can_create_event(self, current_event_count):
        if self.subscription_type == self.NORMAL:
            return False
        elif self.subscription_type == self.SUPER_USER:
            return current_event_count < 50
        elif self.subscription_type == self.PREMIUM:
            return True
        return False

    def activate_subscription(self, subscription_type, duration_in_days=30):
        self.subscription_type = subscription_type
        self.subscription_expiry = datetime.now() + timedelta(days=duration_in_days)
        self.save()