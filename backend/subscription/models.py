from django.db import models
from users.models import CustomUser
from django.db import models
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone


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

    timestamps = models.DateTimeField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription}"
    
    @classmethod
    def get_total_amount(cls):
        # Get the sum of all amounts
        total_amount = cls.objects.aggregate(models.Sum('amount'))['amount__sum']
        return total_amount if total_amount else 0
    
    def is_subscription_valid(self):
        # Get the current timestamp
        current_timestamp = timezone.now()

        # Calculate the difference in days between the current timestamp and the subscription timestamp
        days_difference = (current_timestamp - self.timestamps).days

        # Assuming the subscription is valid for 30 days
        subscription_valid_duration = 30

        # Check if the subscription is still valid
        return days_difference > subscription_valid_duration

    def is_expired(self):
        return not self.is_subscription_valid()
    
    def renew(self):
        # Set the timestamp to the current date and time
        self.timestamp = timezone.now()
        # Save the changes to the database
        self.save()
    


class SubcribedUsers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    is_reneue = models.BooleanField(default=False,null=True,blank=True) 

    subscription_payments = models.ManyToManyField(SubscriptionPayment, related_name='subscribed_users')
