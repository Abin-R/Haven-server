import statistics
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from posts.serializers import *


# Create your views here.

class EventtView(APIView):
    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

class EventDetailView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=statistics.HTTP_404_NOT_FOUND)
    

class EventCreateView(APIView):
    permission_classes = [IsAuthenticated]
    print("---------")
    def post(self, request):
        try:
            print(request.data)
            title = request.data.get('title')
            description = request.data.get('description')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            location = request.data.get('location')
            image = request.data.get('image')
            cost = request.data.get('cost')
            category = request.data.get('category')
            organizer = request.user

            a = SubcribedUsers.objects.get(user = organizer)

            print(organizer)
            # Create a new Country object
            event =  Event (
                title = title,
                description = description,
                start_date = start_date,
                end_date = end_date,
                location = location,
                image = image,
                cost = cost,
                category =category,
                organizer = a
            )
            print(event)

            # Save the object to the database
            event.save()

            # Return a response indicating success
            return Response({'message': 'Country created successfully'}, status=status.HTTP_201_CREATED)# Deserialize the request data using the EventSerializer

        except Exception as e:
            import traceback
            traceback.print_exc()  # Add this line to print the traceback
            # Handle any exceptions (log or customize error response)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = SubcribedUsers.objects.get(user=self.request.user)
        # Fetch events associated with the currently authenticated user
        return Event.objects.filter(organizer=user).order_by('-id')

class CreateBookingView(APIView):
    def post(self, request):
        try:
            print("----------")
            event_title = request.data.get('event').strip()
            prices = request.data.get('prices')
            print(event_title)

            # Fetch the Event by title (case-insensitive)
            a = Event.objects.get(title__iexact=event_title)
            print(a)

            # Create a new transaction
            transaction = Transaction.objects.create(
                user=request.user,
                event = a,
                amount=prices,
                transaction_type='PAYMENT',
                status='PENDING',
            )
            print("Transaction created:", transaction)

            # Create a new booking
            booking = Booking.objects.create(
                user=request.user,
                event=a,
                transaction=transaction,
                booking_status='PENDING',
            )
            print("Booking created:", booking)

            return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AttendeesForEventView(generics.ListAPIView):
    serializer_class = AttendeeSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Booking.objects.filter(event__id=event_id, booking_status='CONFIRMED')
