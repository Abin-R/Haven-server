
from rest_framework import serializers
from subscription.models import *
from events.models import Transaction,Event,Booking
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_type', 'price']

class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    subscription = SubscriptionSerializer()  # Include Subscription data in SubscriptionPaymentSerializer

    class Meta:
        model = SubscriptionPayment
        fields = ['id','user', 'subscription', 'transaction_id', 'amount', 'timestamp', 'timestamps']



class SubcribedUsersSerializers(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = SubcribedUsers
        fields = '__all__'



class EventSerializerss(serializers.ModelSerializer):
    organizer = SubcribedUsersSerializers()
    class Meta:
        model = Event
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    event = EventSerializerss()
    class Meta:
        model = Transaction
        fields = '__all__'



class BookingSerializers(serializers.ModelSerializer):
    user = CustomUserSerializer()
    event = EventSerializerss()
    transaction = TransactionSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class TotalRevenueSerializer(serializers.Serializer):
    totalRevenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class SubcribedUsersSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer() 
       
    class Meta:
        model = SubcribedUsers
        fields = ['user', 'is_premium', 'is_super', 'subscription_payments']

