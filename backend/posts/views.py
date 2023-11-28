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
from events.serializers import *


# Create your views here.
class PostList(generics.ListAPIView):
    queryset = EventPosting.objects.all()
    serializer_class = EventPostingSerializer

class PostDetail(generics.ListAPIView):
    def get(self, request, post_id):
        post = get_object_or_404(EventPosting, id=post_id)
        bookings = Booking.objects.filter(event=post.event)
        event_reviews = EventReview.objects.filter(event=post.event)

        post_serializer = EventPostingSerializer(post)
        bookings_serializer = BookingSerializer(bookings, many=True)
        reviews_serializer = EventReviewSerializer(event_reviews, many=True)

        response_data = {
            'post': post_serializer.data,
            'bookings': bookings_serializer.data,
            'event_reviews': reviews_serializer.data,
        }

        return JsonResponse(response_data)
    
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


class CreateEventReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        postid = request.data.get('postid')
        user = request.user

        # Fetch the Event using postid
        event = get_object_or_404(Event, id=postid)

        # Create EventReview instance
        serializer = EventReviewSerializer(data={
            'user': user.id,
            'event': event.id,
            'rating': request.data.get('rating'),
            'review_text': request.data.get('review_text'),
            'date_created': request.data.get('date_created'),
        })

        if serializer.is_valid():
            serializer.save()

            # Handle images
            image = request.FILES.get("image")
            image_instance = Image.objects.create(image=image)
            serializer.instance.images.add(image_instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(">>>>>>>>>>>>>",self.request.user)
        print("-----------")
        user = CustomUser.objects.get(username=self.request.user)
        print(user)
        # Fetch events associated with the currently authenticated user
        return EventPosting.objects.filter(user=user)
