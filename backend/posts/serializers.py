from rest_framework import serializers
from .models import *
from users.models import *
from events.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with your actual User model
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventPostingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    event = EventSerializer()

    class Meta:
        model = EventPosting
        fields = ['id', 'user', 'event', 'image', 'description', 'completionStatus']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Booking
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class EventReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = EventReview
        fields = ['id', 'user', 'event', 'rating', 'review_text', 'date_created', 'images','user_username']


class PostSerializer(serializers.ModelSerializer):


    class Meta:
        model = EventPosting
        fields = ['id', 'user', 'event', 'image', 'description', 'completionStatus']