# serializers.py

from rest_framework import serializers
from .models import Subscription
from events.models import *




class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscription_type', 'price')


