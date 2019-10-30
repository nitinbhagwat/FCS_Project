from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.groups_view, name="group_view"),
    path('connect/<operation>/<variable>/<pk>', views.group_operations, name="group_operations"),
    path('group_addmember', views.group_addmember, name="group_addmember"),
    ]
