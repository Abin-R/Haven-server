# serializers.py

from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'cost',
            'location',
            'organizer',
            'category',
            'image',
        )

# serializers.py

from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'cost',
            'location',
            'organizer',
            'category',
            'image',
        )

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_date', 'transaction_type', 'status']

class AttendeeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    event = EventSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'transaction', 'booking_status']

    def get_user(self, obj):
        # Define how user information should be serialized
        user_data = {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
        }
        return user_data
