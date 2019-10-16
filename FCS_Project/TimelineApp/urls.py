from django.urls import path
from .views import timeline, latest_post

urlpatterns = [
    path('user/<to_user_name>/', timeline, name='timeline'),
    path('get_latest_post/<to_user_name>/', latest_post, name='timeline_get_latest_post'),
]