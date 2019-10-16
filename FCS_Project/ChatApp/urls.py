from django.urls import path
from .views import chat_function, chats_count_function

urlpatterns = [
    path('user/<user_name>/', chat_function, name='chat'),
    path('get_chats_count/<user_name>/', chats_count_function, name='chats_count'),
]