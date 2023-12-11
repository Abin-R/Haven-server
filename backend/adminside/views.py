from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from users.models import CustomUser
from subscription.models import SubcribedUsers
from .serializer import *
from django.shortcuts import get_object_or_404
from events.models import *
from rest_framework import status
from decimal import Decimal
from django.db.models import Sum
from rest_framework import generics, permissions
from posts.models import *
from posts.serializers import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
from rest_framework.response import Response
from users.serializers import UserSerializers  # Import your CustomUser serializer

class UserList(APIView):
    def get(self, request):
        try:
            userlist = CustomUser.objects.all().order_by('id')
            serialized_users = []

            for user in userlist:
                subscribed_user = SubcribedUsers.objects.filter(user=user).first()
                serialized_user = {
                    'id': user.id,
                    'password': user.password,
                    'username': user.username,
                    'image': user.image.url if user.image else None,
                    'email': user.email,
                    'is_active': user.is_active,
                    'admin': user.is_superuser,
                    'phone': user.phone,
                    'is_super': subscribed_user.is_super if subscribed_user else False,
                    'is_premium': subscribed_user.is_premium if subscribed_user else False,
                }
                serialized_users.append(serialized_user)

            data = {'userlist': serialized_users}
            return JsonResponse(data)

        except Exception as e:
            
            return JsonResponse({'error': str(e)}, status=500)

class SubscriptionListView(APIView):
    def get(self, request):
        try:
            # Fetch all SubscriptionPayment objects
            subscription_payments = SubscriptionPayment.objects.all()

            # Serialize the SubscriptionPayment queryset using the serializer
            subscription_payment_serializer = SubscriptionPaymentSerializer(subscription_payments, many=True)
            subscription_payment_data = subscription_payment_serializer.data

            # Fetch SubscribedUsers instances related to the SubscriptionPayment objects
            subscribed_users_data = []
            for payment in subscription_payments:
                subscribed_users_serializer = SubcribedUsersSerializers(payment.subscribed_users.all(), many=True)
                subscribed_users_data.append(subscribed_users_serializer.data)

            # Combine the SubscriptionPayment and SubscribedUsers data
            for i, payment_data in enumerate(subscription_payment_data):
                payment_data['subscribed_users'] = subscribed_users_data[i]

            # Return the combined data as JSON response
            return Response(subscription_payment_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        


class BlockUser(APIView):
    def post(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            
            # Set is_active to False to block the user
            user.is_active = False
            user.save()

            return JsonResponse({'message': f'User {user.username} blocked successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class UnBlockUser(APIView):
    def post(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            
            # Set is_active to False to block the user
            user.is_active = True
            user.save()

            return JsonResponse({'message': f'User {user.username} blocked successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    
class EventBookingView(APIView):
    def get(self,request):
        try:
            event_booking = Booking.objects.all().order_by('-id')
          

            serializer = BookingSerializers(event_booking, many=True)

            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class ApproveBookingView(APIView):
    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        user = CustomUser.objects.get(username=booking.user)

        email_subject = 'Your Booking Information'
        email_body = render_to_string('booking_email_template.html', {'data': {'bookings': [booking]}})
        plain_text_message = strip_tags(email_body)

        to_email = user.email  # Replace with the actual email field in your CustomUser model

        email = EmailMessage(email_subject, plain_text_message, to=[to_email])
        # email.attach_alternative(email_body, "text/html")
        email.send()

        booking.booking_status = 'CONFIRMED'
        booking.save()

        return Response({'message': 'Booking approved successfully'}, status=status.HTTP_200_OK)
        
    
class EventListView(APIView):
    def get(self,request):
        try:
            event_list = Event.objects.all().order_by('-id')
            

            serializer = EventSerializerss(event_list,many=True) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class EventApprovalView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_object(self):
        id = self.kwargs.get(self.lookup_field)
        return get_object_or_404(self.get_queryset(), id=id)

    def perform_update(self, serializer):
        # Set the is_approved field to True
        serializer.instance.is_approved = True
        serializer.save()
        
class PostListView(APIView):
    def get(self,request):
        try:
            event_list = EventPosting.objects.all().order_by('-id')

            serializer = EventPostingSerializer(event_list ,many=True) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class AdminDashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            total_revenue = Transaction.objects.aggregate(total_revenue=models.Sum('amount'))['total_revenue'] or 0
            total_profit = SubscriptionPayment.get_total_amount()

            total_booking = Transaction.get_total_amount()
            profit = total_profit + Decimal(total_booking / 10)

            user_count = CustomUser.objects.count()

            booking_count = Booking.objects.count()

            latest_subscribed_users = SubscriptionPayment.objects.all().order_by('-timestamp')[:3]


  

            users_serializer = SubscriptionPaymentSerializer(latest_subscribed_users, many=True)

            event_booking = Booking.objects.all()

            booking_serializer = BookingSerializers(event_booking, many=True)


            return Response({
                'profit': profit,
                'totalRevenue': total_revenue,
                'user_count': user_count,
                'booking_count': booking_count,
                'users': users_serializer.data,
                'booking':booking_serializer.data,
            })
        except Exception as e:
           
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SalesDataView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Query the Booking model to get the total amount for each month
            sales_data = Booking.objects.values('event__start_date__month').annotate(total_amount=Sum('transaction__amount'))

            # Map the month number to month name
            month_mapping = {
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
            }

            # Prepare the final sales data
            formatted_sales_data = [
                {'label': month_mapping[entry['event__start_date__month']], 'value': entry['total_amount'] or 0}
                for entry in sales_data
            ]

            # Construct a response in JSON format
            response_data = {'salesData': formatted_sales_data}

            return JsonResponse(response_data)
        except Exception as e:
            
            return JsonResponse({'error': str(e)}, status=500)
        


class RenewSubscriptionView(APIView):
    def post(self, request, subscription_id):
        try:
            # Get the subscription by ID
            subscription = SubscriptionPayment.objects.get(id=subscription_id)
            

            # Check if the subscription is valid (not expired)
            if subscription.is_subscription_valid():
                
                # Renew the subscription (you may need to implement the `renew` method in your model)
                subscribed_members = SubcribedUsers.objects.get(user=subscription.user)

          

                # Update the boolean field to False
                
                if subscribed_members.is_premium:
                   
                    subscribed_members.is_premium =False
                else:
                    
                    subscribed_members.is_super =False
                
                subscribed_members.is_reneue = True

                subscribed_members.save()
                # logout(request.user)
               

                # Send a renewal email to the user
                subject = 'Subscription Renewed'

                context = {'user': subscription.user, 'subscription': subscription}
                html_message = render_to_string('email/renewal_email.html', context)
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = subscription.user.email
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                return Response({'message': 'Subscription renewed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Subscription is not expired'}, status=status.HTTP_400_BAD_REQUEST)
        except SubscriptionPayment.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)


class InvoiceView(APIView):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking_serializer = BookingSerializer(booking)

        transaction = Transaction.objects.get(id=booking.transaction.id)
        transaction_serializer = TransactionSerializer(transaction)

        # Combine the data from both serializers into a dictionary
        response_data = {
            'booking': booking_serializer.data,
            'transaction': transaction_serializer.data,
        }

        # You can customize the response based on your needs
        return JsonResponse(response_data)