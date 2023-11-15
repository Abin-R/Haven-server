
from rest_framework import serializers
from subscription.models import *
from users.serializers import *

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_type', 'price']

class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    subscription = SubscriptionSerializer()  # Include Subscription data in SubscriptionPaymentSerializer

    class Meta:
        model = SubscriptionPayment
        fields = ['user', 'subscription', 'transaction_id', 'amount', 'timestamp']