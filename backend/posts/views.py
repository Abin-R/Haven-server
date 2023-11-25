from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView


# Create your views here.
class PostList(generics.ListAPIView):
    queryset = EventPosting.objects.all()
    serializer_class = EventPostingSerializer

class PostDetail(generics.ListAPIView):
    def get(self, request , post_id):
        print(post_id)
        post = get_object_or_404(EventPosting, id=post_id)
        print(post)
        serializer = EventPostingSerializer(post)  # Assuming you have a serializer for your Post model
        return JsonResponse(serializer.data)
    
class CreatePost(APIView):
    def post(Self,request,post_id):
        try:
            event = Event.objects.get(id = post_id)
            description = request.data.get('description')
            location = request.data.get('location')
            image = request.data.get('image')
            organizer = request.user

            post =  EventPosting (
                
                description = description,
                completionStatus = location,
                image = image,
                event =  event,
                user = organizer
            )
            print("---------",post)

            # Save the object to the database
            post.save()

            return Response({'message': 'Country created successfully'}, status=status.HTTP_201_CREATED)# Deserialize the request data using the EventSerializer

        except Exception as e:
            import traceback
            traceback.print_exc()  # Add this line to print the traceback
            # Handle any exceptions (log or customize error response)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



