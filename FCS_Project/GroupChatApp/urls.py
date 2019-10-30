from django.urls import path
from .views import create_announcement, show_announcements

urlpatterns = [
    path('group/<group_name>/', show_announcements, name='show_announcements'),
    path('create/group/<group_name>/', create_announcement, name='create_announcement'),
]