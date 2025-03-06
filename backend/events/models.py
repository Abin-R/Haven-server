from django.db import models
from subscription.models import SubcribedUsers
from users.models import *

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(SubcribedUsers, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    ticket_count = models.PositiveIntegerField(default=0 ,null=True ,blank=True )
    is_approved = models.BooleanField(default=False ,null=True ,blank=True)   # Add this line

    def __str__(self):
        return self.title

class Transaction(models.Model):
    transaction_type_choices = [
        ('PAYMENT', 'Payment'),
        ('REFUND', 'Refund'),
    ]

    status_choices = [
        ('SUCCESS', 'Success'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    ]

   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE ,null=True,blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True,blank=True) 
    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20, choices=transaction_type_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    

    def __str__(self):
        return f'Transaction {self.pk} - {self.user} for {self.event}'

    @classmethod
    def get_total_amount(cls):
        # Get the sum of all amounts
        total_amount = cls.objects.aggregate(models.Sum('amount'))['amount__sum']
        return total_amount if total_amount else 0


class Booking(models.Model):
    booking_status_choices = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField(default=1)  
    transaction = models.ForeignKey(Transaction ,on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=20, choices=booking_status_choices)
    
    def __str__(self):
        return f'Booking {self.pk} - {self.user} for {self.event}'



