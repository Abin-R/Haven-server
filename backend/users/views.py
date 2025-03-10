from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes , force_str
from .Token import generate_token
from django.core.mail import send_mail , EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from datetime import timedelta
from django.utils import timezone
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from google.auth.transport import requests
from google.oauth2 import id_token
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from subscription.models import SubcribedUsers
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json, razorpay
from django.utils.html import strip_tags


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data['username']
            user = CustomUser.objects.get(username=username)
            role = get_user_role(user)
            reneue = get_is_reneue(user) 

            response.data['username'] = username
            response.data['role'] = role
            response.data['reneue'] = reneue
            response.data['userId'] = user.id  # Include user ID in the response
            response.data['profileImage'] = str(user.image.url) if user.image else None

        return response

class RegisterView(APIView):
    def post(self, request):
        try:
            print(1)
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
                return Response({'message': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            myuser=CustomUser.objects.create_user(username=username, password=password, email=email)
            myuser.is_active = False
            myuser.save()

            current_site = get_current_site(request)    
            email_subject = 'confirm Your email @ Haven'
            message2 = render_to_string('activation_mail.html',{
                'name': myuser.username ,
                'domain': current_site.domain ,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            email = EmailMessage(
                email_subject,message2,
                settings.EMAIL_HOST_USER,
                [myuser.email] 
            )
            email.fail_silently = True
            email.send()

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GoogleAuthAPIView(APIView):
    
    def post(self, request):
        token = request.data.get('idToken')
        email = request.data.get('email')
        username = request.data.get('username')

        try:
            CLIENT_ID = '591332327561-qqkbkghu0ddnmngvju4e1s9jgfi4rj44.apps.googleusercontent.com'  # Replace with your Google OAuth Client ID

            # Verify the token with the Google Auth library
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            existing_user = CustomUser.objects.filter(email=email).first()

            if existing_user:
                # User with this email exists in the backend
                access_token = RefreshToken.for_user(existing_user)
                access_token = str(access_token.access_token)

                # Generate Refresh Token
                refresh_token = RefreshToken.for_user(existing_user)
                refresh_token = str(refresh_token)
                role = get_user_role(existing_user)

                response_data = {
                    'message': 'User exists in the backend',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'username': username,
                    'role':role,
                    # Add other necessary details to the response
                }
               

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # User does not exist in the backend, create a new user
                new_user = CustomUser.objects.create(username=username, email=email)
                
                # You might want to add more fields to the new user as needed

                # Generate Access Token for the new user
                access_token = RefreshToken.for_user(new_user)
                access_token = str(access_token.access_token)

                # Generate Refresh Token for the new user
                refresh_token = RefreshToken.for_user(new_user)
                refresh_token = str(refresh_token)
                role = get_user_role(new_user)
                response_data = {
                    'message': 'User created and tokens generated',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'username': username,
                    'role':role,
                    # Add other necessary details to the response
                }
                send_mail(
                    f'Hi {username}',
                    f'You have successfully created an account in Haven Association. Your username is {username}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [new_user.email],
                    fail_silently=False,
                )


                return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            # Handle any verification errors
            return Response({'error': 'Token verification failed'}, status=status.HTTP_401_UNAUTHORIZED)







class Activate(APIView):
     
     def post(self, request):
          otp = request.data.get('otp')
          username = request.data.get('username')
          generated_otp = request.session.get('otp')
        
          if otp == generated_otp:
               try:
                    
                    myuser = CustomUser.objects.get(username=username)
                    myuser.is_active = True
                    myuser.save()
               except CustomUser.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
               
               # Delete the OTP from the session
               del request.session['otp']

               # You can send a success response with user data if needed
               # For example, you can send the user's username or ID
               return Response({'message': 'OTP successfully validated'}, status=status.HTTP_200_OK)
          else:
               return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
               



def activate(request,uidb64,token):
     try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=CustomUser.objects.get(pk=uid)
     except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None
      # checking the user and token doesnt has a conflict  
     if myuser is not None and generate_token.check_token(myuser,token):
        
        myuser.is_active=True
        session=settings.SITE_URL + '/login'
     #    return render(request,'verification_success.html')
        if myuser.date_joined > timezone.now() - timedelta(hours=24):
            myuser.save()
        # myuser.save()
        return HttpResponseRedirect(session)        
     else:
        # Delete the user if activation fails and the activation link is expired
        user_creation_time = myuser.date_joined
        # Define the expiration time (24 hours after user creation)
        expiration_time = user_creation_time + timedelta(hours=24)  

        if myuser is not None and myuser.is_active == False and timezone.now() > expiration_time:
            myuser.delete()

        return render(request, 'verification_failed.html')    




class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'message': 'Refresh token is missing'}, status=status.HTTP_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            
            token.blacklist()

            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
           
            return Response({'message': 'Invalid token or an error occurred'}, status=status.HTTP_400_BAD_REQUEST)



  
class ForgetPasswordEmailView(APIView):
     def post(self,request):
          try:
               email = request.data.get('email')   
               myuser=CustomUser.objects.get(email=email)
            
               
               current_site = get_current_site(request)
               email_subject = 'confirm Your email @ Haven Association'
               message2 = render_to_string('forgot_password_mail.html',{
                    'name': myuser.username ,   
                    'domain': current_site.domain ,
                    'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                    'token': generate_token.make_token(myuser),
               })
               email = EmailMessage(
                    email_subject,message2,
                    settings.EMAIL_HOST_USER,
                    [myuser.email] 
               )
               email.fail_silently = True
               email.send()

               return Response({'message': 'email sent successfully'}, status=status.HTTP_200_OK)
          except Exception as e:
               # Handle exceptions here and return an appropriate error response
               return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
               
def forgot_password_mail_view(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=CustomUser.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser,token):
        session = 'http://localhost:5173/reset-password/?uidb64=' + uidb64
        return HttpResponseRedirect(session)        
     
class ResetPassword(APIView):
     def post(self,request):
          password = request.data.get('password')
          uidb64 = request.data.get('uidb64')
          try:
               uid=force_str(urlsafe_base64_decode(uidb64))
               myuser=CustomUser.objects.get(pk=uid)
          except(TypeError,ValueError,OverflowError, User.DoesNotExist):
               myuser=None
          if myuser is not None:
            # Set the new password for the user
            myuser.set_password(password)
            myuser.save()

            return JsonResponse({'message': 'Password reset successfully'}, status=200)
          else:
            return JsonResponse({'error': 'Invalid or expired reset link'}, status=400)


class ProfileView(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        try:
            # Assuming there is a ForeignKey from Booking to CustomUser
            profile = CustomUser.objects.get(username=username)
            bookings = Booking.objects.filter(user=profile)

            # Serialize the user profile
            user_serializer = UserSerializers(profile)

            # Serialize the bookings
            booking_serializer = BookingSerializer(bookings, many=True)

            # Create a dictionary with both serializers' data
            response_data = {
                'user_profile': user_serializer.data,
                'bookings': booking_serializer.data,
            }

            

            return Response(response_data)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Booking.DoesNotExist:
            return Response({'error': 'Bookings not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):
    profile = CustomUser.objects.get(username=request.user)
   

    if 'profileImage' in request.FILES:
        profile.image = request.FILES['profileImage']
        profile.save()

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    else:
        return Response({'error': 'No image file provided'}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_profile(request):
    try:
        data = json.loads(request.body)
        
        username = data.get('username') 
      
        user = CustomUser.objects.filter(username=username).first()
        # Update user fields based on the received data
        user.username = data.get('username', user.username)
        user.address = data.get('address', user.address)
        user.country = data.get('country', user.country)
        user.zipcode = data.get('zipcode', user.zipcode)

        # Save the updated user
        user.save()

        return JsonResponse({'message': 'Profile updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class CreateOrder(APIView):
    def post(self, request, *args, **kwargs):
        try:
            amount = request.data.get("amount")
            razorpay_client = razorpay.Client(auth=("rzp_test_dQb1h6OwivRNsS", "lY1M7VYj2jmnQrOibpTf4cDZ"))

            order = razorpay_client.order.create(dict(
                amount=amount, 
                currency="INR",
                payment_capture="1",
            ))
            return Response({"order_id": order["id"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SaveSubscription(APIView):
    def post(self, request, *args, **kwargs):
        subscription_type = request.data.get('subscriptionType')
        username = request.data.get('username')
        valid_types = [CustomUser.NORMAL, CustomUser.SUPER_USER, CustomUser.PREMIUM]
        if subscription_type not in valid_types:
            return JsonResponse({'error': 'Invalid subscription type'}, status=400)

        user = CustomUser.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        user.subscription_type = subscription_type
        user.save()

        subscribed_user, created = SubcribedUsers.objects.get_or_create(user=user)
        if subscription_type in ['super', 'premium']:
                if subscription_type == 'super':
                    subscribed_user.is_super = True
                elif subscription_type == 'premium':
                    subscribed_user.is_premium = True
                subscribed_user.is_reneue = False

                subscribed_user.save()

        return JsonResponse({'message': 'Subscription updated successfully', 'subscription_type': user.subscription_type})