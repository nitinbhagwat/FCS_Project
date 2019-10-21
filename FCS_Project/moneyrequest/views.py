from django.db.models import Subquery
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView

from django.contrib.auth.models import User
# Create your views here.
import Authentication
from Authentication.models import CustomUser
from friends.models import Friend
from moneyrequest.models import MoneyRequest
from Transactions.views import send_money
from Transactions.models import Transactions
from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime, time, timedelta
import pytz


from django.contrib.auth.decorators import login_required


@login_required(login_url="/users/login/")
def request_view(request):

    if request.method == "POST":
        name_entered = request.POST.get("myText", None)
        price_entered = request.POST.get("priceText", None)
        func(request, name_entered, price_entered)

    cansend1 = MoneyRequest.objects.filter(sendername=request.user.username)
    cansend = Friend.objects.filter(sendername=request.user.username).exclude(recievername__in=Subquery(cansend1.values('recievername')))

    requestrecieved = MoneyRequest.objects.filter(recievername=request.user.username)

    return render(request, 'moneyrequest/moneyrequest.html', {'cansend': cansend, 'requestrecieved': requestrecieved})


@login_required
def request_friends(request, operation, pk, money):

    print (pk)
    if operation == 'accept':
        # TODO: Nitin
        from_username = request.user.username
        to_username = pk
        amount = float(money)
        if amount <= 0.0:
            return HttpResponse ("Amount should be greater than 0.")

        wallet_balance = request.user.uWalletBalance
        transaction_count = request.user.uTransactionNumber
        max_transactions_count = 99999
        if request.user.role == 'casual':
            max_transactions_count = 15
        elif request.user.role == 'premium':
            max_transactions_count = 30 

        if wallet_balance >= amount and transaction_count < max_transactions_count:
            transaction_obj = Transactions()
            transaction_obj.to_username = to_username
            transaction_obj.from_username = from_username
            transaction_obj.amount = amount
            exception = send_money(amount, to_username, from_username, None)
            if exception:
                return HttpResponse(exception)
            else:
                transaction_obj.save()
        else:
            return HttpResponse ("Either you have not enough balance to process this request or you have exceeded your maximum transaction limit.")
        MoneyRequest.accept(request.user.username, pk)

    elif operation == 'reject':
        MoneyRequest.reject(request.user.username, pk)

    return redirect('/moneyrequest')


def func(request,friend_name,money):
    MoneyRequest.send(request.user.username,friend_name,money)
