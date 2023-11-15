# urls.py in subscription app

from django.urls import path
from .views import *

urlpatterns = [
    path('save-subscription/', SaveSubscription.as_view(), name='save_subscription'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    

]
