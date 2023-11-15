from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import CustomUser
from .models import *
from rest_framework import status
from .serializers import SubscriptionSerializer


class SubscriptionListView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
    
class SaveSubscription(APIView):
    def post(self, request):
        print("hiiiiiiiiiii")

        username = request.data.get('username') 
        print(username)
        user = CustomUser.objects.filter(username=username).first()

        if user:
            subscription_type = request.data.get('subscriptionType')
            subscribed_user, created = SubcribedUsers.objects.get_or_create(user=user)

            if subscription_type in ['super', 'premium']:
                if subscription_type == 'super':
                    subscribed_user.is_super = True
                elif subscription_type == 'premium':
                    subscribed_user.is_premium = True

                subscribed_user.save()

                # Save subscription payment details
                subscription = Subscription.objects.get(subscription_type=subscription_type)  # Get the Subscription object
                transaction_id = request.data.get('transactionId')  # Replace with the actual transaction ID
                amount = request.data.get('amount')  # Replace with the actual subscription amount

                subscription_payment = SubscriptionPayment.objects.create(
                    user=user,
                    subscription=subscription,
                    transaction_id=transaction_id,
                    amount=amount
                )

                # Set user role based on subscription
                if subscription_type == 'super':
                    user_role = 'super'
                elif subscription_type == 'premium':
                    user_role = 'premium'
                else:
                    user_role = 'user'

                # Include username and user ID in the response
                return Response({'message': 'Subscription and payment saved successfully', 'user_role': user_role, 'username': user.username, 'userId': user.id}, status=status.HTTP_200_OK)
            else:
                return Response('Invalid subscription type', status=status.HTTP_400_BAD_REQUEST)

        return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)


