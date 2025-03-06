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
from datetime import datetime


# Create your views here.

class EventtView(APIView):
    def get(self, request):
        current_datetime = datetime.now()
        # Filter events that are approved by an admin
        events = Event.objects.filter(end_date__gte=current_datetime, is_approved=True)
      
        serializer = EventSerializer(events, many=True)
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

    def post(self, request):
        try:
         
            title = request.data.get('title')
            description = request.data.get('description')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            location = request.data.get('location')
            image = request.data.get('image')
            cost = request.data.get('cost')
            category = request.data.get('category')
            ticket_count = request.data.get('ticket_count')
            organizer = request.user

            a = SubcribedUsers.objects.get(user = organizer)

           
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
                organizer = a,
                ticket_count = ticket_count,
                is_approved = True
            )
          

            # Save the object to the database
            event.save()

            # Return a response indicating success
            return Response({'message': 'Country created successfully'}, status=status.HTTP_201_CREATED)# Deserialize the request data using the EventSerializer

        except Exception as e:
            import traceback
            traceback.print_exc()  # Add this line to print the traceback
            # Handle any exceptions (log or customize error response)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class EventEditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            # Fetch the event by ID
            event = Event.objects.get(id=event_id)
            # Serialize the event data
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, event_id):
        try:
            # Fetch the event by ID
            event = Event.objects.get(id=event_id)

            # Deserialize the request data using the EventSerializer
            serializer = EventSerializer(instance=event, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Extract additional data from the request
            ticket_count = request.data.get('ticket_count', 0)

            # Update the event object
            serializer.save(ticket_count=ticket_count)

            # Return a response indicating success
            return Response({'message': 'Event updated successfully'}, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = SubcribedUsers.objects.get(user=self.request.user)
        # Fetch events associated with the currently authenticated user
        return Event.objects.filter(organizer=user).order_by('-id')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Booking, Transaction
from django.shortcuts import get_object_or_404

class CreateBookingView(APIView):
    def post(self, request):
        try:
            event_title = request.data.get('event').strip()
            prices = request.data.get('prices')
            ticket_count = request.data.get('ticket', 1)  # Default to 1 if not provided

            # Fetch the Event by title (case-insensitive)
            event = get_object_or_404(Event, title__iexact=event_title)

            # Ensure there are enough tickets available
            if event.ticket_count < ticket_count:
                return Response({'error': 'Not enough tickets available'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new transaction
            transaction = Transaction.objects.create(
                user=request.user,
                event=event,
                amount=prices,
                transaction_type='PAYMENT',
                status='SUCCESS',
            )

            # Create a new booking
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                transaction=transaction,
                booking_status='PENDING',
                ticket_count = ticket_count,
            )

            # Reduce the ticket count
            event.ticket_count -= ticket_count
            event.save()

            return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class AttendeesForEventView(generics.ListAPIView):
    serializer_class = AttendeeSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Booking.objects.filter(event__id=event_id, booking_status='CONFIRMED')
