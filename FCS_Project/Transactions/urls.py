from django.contrib import admin
from django.urls import path, include

# import your required views first
from Transactions.views import make_transaction

urlpatterns = [
    
    path('', make_transaction),
    
]