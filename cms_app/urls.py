# cms_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Blog endpoints
    path('', blog_list_create, name='blog-list-create'),
    path('<int:pk>/',blog_detail, name='blog-detail'),
    
    # Like endpoints
    path('like/<int:blog_id>/', toggle_like, name='like-post'),
    
    # Additional utility endpoints
    path('my-posts/', get_user_posts, name='user-posts'),
    # path('my-likes/', get_user_likes, name='user-likes'),
    path('<int:blog_id>/likes/', get_post_likes, name='post-likes'),
]

