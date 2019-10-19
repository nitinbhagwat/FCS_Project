from django.db.models import Subquery
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView

from django.contrib.auth.models import User
# Create your views here.
import Authentication
from Authentication.models import CustomUser
from friends.models import Friend
from moneyrequest.models import MoneyRequest

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


def request_friends(request, operation, pk, money):

    if operation == 'accept':
        # TODO: Nitin
        MoneyRequest.accept(request.user.username, pk)

    elif operation == 'reject':
        MoneyRequest.reject(request.user.username, pk)

    return redirect('/moneyrequest')


def func(request,friend_name,money):
    MoneyRequest.send(request.user.username,friend_name,money)
