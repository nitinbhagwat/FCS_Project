from django.contrib import admin
from django.urls import path, include

# import your required views first
from Transactions.views import make_transaction, verify_otp, add_money_in_wallet, verify_otp_for_add_money


urlpatterns = [
    
    path('', make_transaction),
    path('add-money/', add_money_in_wallet, name='Add Money'),
    path('connect/', verify_otp, name="verify_otp"),
    # ???? Below
    path('add-money/connect/', verify_otp_for_add_money, name="verify_otp_for_add_money"),
]