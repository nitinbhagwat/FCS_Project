from django.urls import path
from .views import create_page, show_pages, show_commercial_user

urlpatterns = [
    path('show_users/', show_commercial_user, name='show_commercial_user'),
    path('user/<user_name>/', show_pages, name='show_pages'),
    path('create/', create_page, name='create_page'),
]