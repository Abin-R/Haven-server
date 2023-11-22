# urls.py in subscription app

from django.urls import path
from .views import *

urlpatterns = [

    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:post_id>/',PostDetail.as_view(), name='get_post_detail'),
    path('posts/<int:post_id>/',CreatePost.as_view(), name='get_post_detail'),
    

    
    

]