import django
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.db.models import Subquery
from django.contrib.auth.models import User
# Create your views here.
import Authentication
from Authentication.models import CustomUser
from friends.models import Friend

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST

@csrf_protect
@requires_csrf_token
@login_required(login_url="/users/login/")
def friends_view(request):
    global original_password

    # users = CustomUser.objects.exclude(username=request.user.username)
    users1 = Friend.objects.filter(sendername=request.user.username)
    users = CustomUser.objects.exclude(username__in=Subquery(users1.values('recievername'))).exclude(username=request.user.username)
    friends = Friend.objects.filter(sendername=request.user.username).exclude(status=0).exclude(status=-1)
    friends_mine = Friend.objects.filter(recievername=request.user.username).exclude(status=-1).exclude(status=1)

    return render(request, 'friends/friends.html', {'users': users, 'friends': friends, 'friends_mine': friends_mine})

@csrf_protect
@requires_csrf_token
@login_required(login_url="/users/login/")
def change_friends(request, operation, pk):

    if request.method == 'POST':

        if request.user.username == pk:
            return HttpResponse("Invalid Request")

        else:
            if operation == 'add':
                Friend.make_friend(request.user.username, pk)

            elif operation == 'accept':
                Friend.accept_friend(request.user.username, pk)

            elif operation == 'remove':
                Friend.loose_friend(request.user.username, pk)

            elif operation == 'reject':
                Friend.reject_friend(request.user.username, pk)

            return redirect('/show_friends')

    else:
        return render(None, 'error_type1.html')
