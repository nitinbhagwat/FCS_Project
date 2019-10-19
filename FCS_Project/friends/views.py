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


@login_required(login_url="/users/login/")
def friends_view(request):
    global original_password

    # users = CustomUser.objects.exclude(username=request.user.username)
    users1 = Friend.objects.filter(sendername=request.user.username)
    users = CustomUser.objects.exclude(username__in=Subquery(users1.values('recievername'))).exclude(username=request.user.username)
    friends = Friend.objects.filter(sendername=request.user.username).exclude(status=0).exclude(status=-1)
    friends_mine = Friend.objects.filter(recievername=request.user.username).exclude(status=-1).exclude(status=1)

    # if request.method == "POST":
    #     otp_entered = request.POST.get("myText", None)
    #     seekpassword = OTP.objects.filter(email=request.user.email)

    #     for var in seekpassword:
    #         original_password = var.onetimepassword

    #     Func_otp(int(otp_entered), int(original_password), request.user.email)

    return render(request, 'friends/friends.html', {'users': users, 'friends': friends, 'friends_mine': friends_mine})


def change_friends(request, operation, pk):
    friend = CustomUser.objects.filter(pk=pk)

    if operation == 'add':
        Friend.make_friend(request.user.username, pk)

    elif operation == 'accept':
        Friend.accept_friend(request.user.username, pk)

    elif operation == 'remove':
        Friend.loose_friend(request.user.username, pk)

    elif operation == 'reject':
        Friend.reject_friend(request.user.username, pk)

    # elif operation == 'generate':
    #     OTP.generate_OTP(request.user.email)
    #     Func_sendmail(request, request.user.email)


    return redirect('/show_friends')


# def Func_otp(otp_entered, original_otp, email):
#     if otp_entered == original_otp:
#         print('CORRECT')
#         OTP.verified_OTP(email)
#     else:
#         print('Incorrect')


# def Func_sendmail(request, rec_id):
#     seekpassword1 = OTP.objects.filter(email=request.user.email)

#     for var1 in seekpassword1:
#         send_otp = var1.onetimepassword

#     subject = 'Verification OTP'
#     # str1 = 'Your OTP for verification is below. Donot share with anyone '
#     # str2 = send_otp
#     # str1.join(str2)

#     message = str(send_otp)
#     from_email = settings.EMAIL_HOST_USER
#     to_list = [request.user.email]

#     print(message)
#     send_mail(subject, message, from_email, to_list, fail_silently=True)
#     # send_mail(subject, message, from_email, to_email, fail_silently= True)

