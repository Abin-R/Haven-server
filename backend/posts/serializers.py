from rest_framework import serializers
from .models import EventPosting
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
