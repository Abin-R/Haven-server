# urls.py in subscription app

from django.urls import path
from .views import *

urlpatterns = [

    path('posts/', PostList.as_view(), name='post-list'),
    path('user-posts/', UserPostsView.as_view(), name='user-posts'),
    path('posts/<int:post_id>/',PostDetail.as_view(), name='get_post_detail'),
    path('create-post/<int:post_id>/',CreatePost.as_view(), name='get_post_detail'),
    path('create-event-review/', CreateEventReview.as_view(), name='create-event-review'),
    path('get-images/', get_images, name='get_images'),
    

    
    

]