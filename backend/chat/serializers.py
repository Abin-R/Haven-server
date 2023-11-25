from rest_framework import serializers
from .models import Message
from users.serializers import * 

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageSerializers(serializers.ModelSerializer):
    # Override the sender field to use the username
    sender = serializers.SerializerMethodField()
    

    class Meta:
        model = Message
        fields = '__all__'

    def get_sender(self, obj):
        # Retrieve the username from the CustomUser sender field
        return obj.sender.username