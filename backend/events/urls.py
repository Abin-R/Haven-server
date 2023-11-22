# urls.py in subscription app

from django.urls import path
from .views import *

urlpatterns = [
    path('events/', EventtView.as_view(), name='event'),
     path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
     path('create-event/', EventCreateView.as_view(), name='event-create'),
     path('user-events/', UserEventsView.as_view(), name='user-events'),
     path('bookings/', CreateBookingView.as_view(), name='create_booking'),
     path('attendees/<int:event_id>/', AttendeesForEventView.as_view(), name='attendees_for_event'),

    
    

]