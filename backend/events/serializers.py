# serializers.py

from rest_framework import serializers
from .models import *
from posts.models import *

class EventSerializer(serializers.ModelSerializer):
    is_in_event_posting = serializers.SerializerMethodField()

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
            'is_in_event_posting',  # Include the new field in the serialized output
        )

    def get_is_in_event_posting(self, obj):
        # Check if there are any EventPosting instances related to the current Event
        return EventPosting.objects.filter(event=obj).exists()


# serializers.py

from rest_framework import serializers
from .models import *

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = (
#             'id',
#             'title',
#             'description',
#             'start_date',
#             'end_date',
#             'cost',
#             'location',
#             'organizer',
#             'category',
#             'image',
#         )

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
