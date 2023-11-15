from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('subscription-list/', SubscriptionListView.as_view() ,name='subscription-list'),
    path('block-user/<int:user_id>/', BlockUser.as_view(), name='block_user'),
    path('unblock-user/<int:user_id>/', UnBlockUser.as_view(), name='block_user'),
    
]