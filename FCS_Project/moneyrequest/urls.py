from django.urls import path
from . import views

app_name = 'moneyrequest'

urlpatterns = [
    path('', views.request_view),
    path('connect/<operation>/<pk>/<money>', views.request_friends, name="request_friends"),
]
