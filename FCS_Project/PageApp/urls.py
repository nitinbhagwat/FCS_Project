from django.urls import path
from .views import create_page, show_pages

urlpatterns = [
    path('user/<user_name>/', show_pages, name='show_pages'),
    path('create/', create_page, name='create_page'),
]