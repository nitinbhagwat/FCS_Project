from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.groups_view, name="group_view"),
    path('connect/<operation>/<variable>/<pk>', views.group_operatioms, name="group_operations"),
    ]
