# cms_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('',api_root,name="api-root"),
    path('accounts/', accounts, name='accounts-view'),     
    path('accounts/login/',login, name='login'),
    path('accounts/logout/',logout, name='logout'),
    path('accounts/refresh/',refresh_access_token, name='refresh'),
    path('me/', get_user_profile, name='user-profile'),
    
]

