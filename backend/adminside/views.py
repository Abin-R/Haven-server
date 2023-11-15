from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from users.models import CustomUser
from subscription.models import SubcribedUsers
from .serializer import *
from django.shortcuts import get_object_or_404

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

            # Serialize the queryset using the serializer
            serializer = SubscriptionPaymentSerializer(subscription_payments, many=True)

            # Return the serialized data as JSON response
            return Response(serializer.data)
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