from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('event-boooking/', EventBookingView.as_view(), name='event_booking'),
    path('invoice/<int:booking_id>/', InvoiceView.as_view(), name='invoice-view'),
    path('approve-booking/<int:booking_id>/', ApproveBookingView.as_view(), name='approve-booking'),
    path('subscription-list/', SubscriptionListView.as_view() ,name='subscription-list'),
    path('event-list/', EventListView.as_view() ,name='event_list'),
    path('post-list/', PostListView.as_view() ,name='post_list'),
    path('event/<int:id>/approve/', EventApprovalView.as_view(), name='event-approve'),
    path('admin-dashboard/', AdminDashboard.as_view(),name='admin_dashboard'),
    path('block-user/<int:user_id>/', BlockUser.as_view(), name='block_user'),
    path('unblock-user/<int:user_id>/', UnBlockUser.as_view(), name='block_user'),
    path('sales-data/', SalesDataView.as_view(), name='sales_data'),
     path('renew-subscription/<int:subscription_id>/', RenewSubscriptionView.as_view(), name='renew-subscription'),
    
]