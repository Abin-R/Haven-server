from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('register/', RegisterView.as_view() , name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', views.activate ,name='activate'),
    path('forgot-password/', views.ForgetPasswordEmailView.as_view(), name='forget_password'),
    path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    path('forgot_password_mail/<str:uidb64>/<str:token>/', views.forgot_password_mail_view, name='forgot_password_mail'),
    path('google-auth/', GoogleAuthAPIView.as_view(), name='google-auth'),
    path('profiles/', ProfileView.as_view(), name='profile-view'),
    # path('login', LoginView.as_view()),
    path('token/', 
          CustomTokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh')

]