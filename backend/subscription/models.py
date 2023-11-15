from django.db import models
from users.models import CustomUser
from django.db import models
from django.contrib.auth.models import User
from .models import *


class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('super', 'Super'),
        ('premium', 'Premium'),
    ]

    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.get_subscription_type_display()} - {self.price}"





class SubscriptionPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # If using Django's built-in User model
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.subscription_type}"
    


class SubcribedUsers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)

    subscription_payments = models.ManyToManyField(SubscriptionPayment, related_name='subscribed_users')
