from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from .serializers import *
from datetime import datetime
from users.models import CustomUser

@api_view(['POST'])
def save_message(request):
    timestamp = datetime.now().isoformat()
    username = request.data.get('user')
    sender = CustomUser.objects.get(username=username)
    message_content = request.data.get('message')

    data = {'sender': sender.pk, 'message_content': message_content, 'timestamp': timestamp}
    serializer = MessageSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)




@api_view(['GET'])
def get_messages(request):
    messages = Message.objects.all()
    serializer = MessageSerializers(messages, many=True)
    return Response(serializer.data)
