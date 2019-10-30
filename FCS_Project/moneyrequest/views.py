from django.db.models import Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.views.generic import TemplateView
from django.contrib.auth.models import User
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


@csrf_protect
@requires_csrf_token
@login_required(login_url="/users/login/")
def request_view(request):
    if request.method == "POST":
        name_entered = request.POST.get("myText", None)
        price_entered = request.POST.get("priceText", None)

        if price_entered.isalpha() or len(name_entered) > 10 or int(price_entered) <= 0 or len(name_entered) <= 0:
            return render(None, 'error_type1.html')

        elif name_entered == request.user.username:
            return HttpResponse('You cannot request money to yourself')
        else:
            if CustomUser.objects.exclude(username=request.user.username).filter(username=name_entered).exists():
                var1 = func(request, name_entered, price_entered)
            else:
                return HttpResponse('No such user ')

            if var1 == 1:
                return HttpResponse('Person you are requesting to is not your friend :(')

    cansend1 = MoneyRequest.objects.filter(sendername=request.user.username)
    cansend = Friend.objects.filter(sendername=request.user.username).exclude(
        recievername__in=Subquery(cansend1.values('recievername'))).filter(status=1)

    requestrecieved = MoneyRequest.objects.filter(recievername=request.user.username)

    return render(request, 'moneyrequest/moneyrequest.html', {'cansend': cansend, 'requestrecieved': requestrecieved})


@csrf_protect
@requires_csrf_token
@login_required(login_url="/users/login/")
def request_friends(request, operation, pk, money):
    if request.method == 'POST':

        if operation == 'accept':
            from_username = request.user.username
            to_username = pk
            amount = float(money)
            if amount <= 0.0:
                return HttpResponse("Amount should be greater than 0.")

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
                exception = send_money(amount, to_username, from_username, None, None)
                if exception:
                    return HttpResponse(exception)
                else:
                    transaction_obj.save()
            else:
                return HttpResponse(
                    "Either you have not enough balance to process this request or you have exceeded your maximum transaction limit.")
            MoneyRequest.accept(request.user.username, pk)

        elif operation == 'reject':
            MoneyRequest.reject(request.user.username, pk)

        return redirect('/moneyrequest')
    else:
        return render(None, 'error_type1.html')


def func(request, friend_name, money):
    friendlist = []

    cansend2 = MoneyRequest.objects.filter(sendername=request.user.username)
    cansend3 = Friend.objects.filter(sendername=request.user.username).exclude(
        recievername__in=Subquery(cansend2.values('recievername')))

    for var in cansend3:
        friendlist.append(var.recievername)

    if friend_name == request.user.username:
        print('You cannot send request to yourself ')
        return render(None, 'error_type1.html')

    elif friend_name not in friendlist:
        print('Name entered not in Friendlist ')
        return 1

    else:
        MoneyRequest.send(request.user.username, friend_name, money)