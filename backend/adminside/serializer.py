
from rest_framework import serializers
from subscription.models import *
from users.serializers import *
from events.models import *

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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    event = EventSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = Booking
        fields = '__all__'