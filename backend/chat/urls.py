# urls.py in subscription app

from django.urls import path
from .views import *
from django.urls import path
from .views import save_message

urlpatterns = [

    
   path('save-message/', save_message, name='save_message'),
   path('get-messages/', get_messages, name='get_messages'),

    
    

]