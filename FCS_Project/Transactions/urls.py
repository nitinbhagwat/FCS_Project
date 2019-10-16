from django.contrib import admin
from django.urls import path, include

# import your required views first
from Transactions.views import make_transaction, verify_otp


urlpatterns = [
    
    path('', make_transaction),
    path('connect/', verify_otp, name="verify_otp"),
    
]