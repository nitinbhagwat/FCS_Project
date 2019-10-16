from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.friends_view, name="friendslist"),
    path('connect/<operation>/<pk>', views.change_friends, name="change_friends"),
]
