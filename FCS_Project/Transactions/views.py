from django.shortcuts import render, redirect
from Transactions.forms import TransactionForm, AddMoneyForm
from django.http import HttpResponse
from django.forms import ValidationError
from Authentication.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db import transaction
from Authentication.models import OTP
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, time, timedelta
import pytz


# Create your views here.


# @login_required
# def deposit(amount, username):
# 	try:
# 		with transaction.atomic():
# 			user = CustomUser.objects.select_for_update().get(username = username)
# 			user.uWalletBalance += amount
# 			user.save()

# 	except Exception as e:
# 		print ("Error: ", e)
# 		raise 


# @login_required
# def withdraw(amount, username):
# 	try:
# 		with transaction.atomic():
# 			user = CustomUser.objects.select_for_update().get(username = username)
# 			user.uWalletBalance -= amount
# 			user.save()

# 	except Exception as e:
# 		print ("Error: ", e)
# 		raise 

# 2-----Upgrade

@login_required
def verify_otp(request):
    OTP.generate_OTP(request.user.email, 0)
    Func_sendmail(request, request.user.email, 0)
    return redirect('/transactions')


@login_required
def verify_otp_for_add_money(request):
    OTP.generate_OTP(request.user.email, 1)
    Func_sendmail(request, request.user.email, 1)
    return redirect('/transactions/add-money')


@login_required
def verify_otp_for_upgrade(request):
    OTP.generate_OTP(request.user.email, 2)
    Func_sendmail(request, request.user.email, 2)
    return redirect('/users/upgrade-account/')


def Func_otp(otp_entered, original_otp, email):
    if otp_entered == original_otp:
        print('CORRECT')
        OTP.verified_OTP(email)
    else:
        print('Incorrect......')
        return HttpResponse("OTP is not verified.")


@login_required
def upgrading(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp_field2", None)
        seekpassword = OTP.objects.filter(email=request.user.email).filter(mode=2)

        if not otp_entered:
            return HttpResponse("You have to enter OTP.")

        if not seekpassword:
            return HttpResponse("You have not generate OTP")

        for var in seekpassword:
            original_otp = var.onetimepassword
            time_then = var.generationtime

        utc = pytz.UTC
        if int(otp_entered) == int(original_otp):
            print("OTP Verified")
            table_expired_datetime = time_then + timedelta(minutes=10)
            time_now = datetime.now()

            expired_on = table_expired_datetime.replace(tzinfo=utc)
            checked_on = time_now.replace(tzinfo=utc)

            if expired_on < checked_on:
                OTP.verified_OTP(request.user.email, 2)
                return HttpResponse(
                    "OTP time expired. Please generate OTP again and then try again.")
            else:
                transaction_count = request.user.uTransactionNumber
                amount = 5000
                username = request.user.username
                max_transactions_count = 30

                if request.user.uWalletBalance >= amount and transaction_count < max_transactions_count:
                    withdraw(amount, username, 'commercial', None)
                else:
                    return HttpResponse(
                        'Either you do not have enough balance to upgrade your account or you cannot make this transaction because limit exceeded.')

                # return HttpResponse ('Your account has been upgraded')
                return redirect('/')
        else:
            return HttpResponse("Your OTP is Incorrect :( ")

    else:
        return render(None, 'error_type1.html')


def Func_sendmail(request, rec_id, type):
    seekpassword1 = OTP.objects.filter(email=request.user.email).filter(mode=type)

    for var1 in seekpassword1:
        send_otp = var1.onetimepassword

    subject = 'Verification OTP'

    if type == 0:
        str1 = 'For sending money: '
    elif type == 2:
        str1 = 'For Upgrading account : '
    elif type == 1:
        str1 = 'For adding money: '

    message1 = str(send_otp)
    message = str1 + message1
    from_email = settings.EMAIL_HOST_USER
    to_list = [request.user.email]

    print(message)
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    # send_mail(subject, message, from_email, to_email, fail_silently= True)


@transaction.atomic
def send_money(amount, to_username, from_username, email, type):
    try:
        print('send money func')
        to_user = CustomUser.objects.select_for_update().get(username=to_username)
        to_user.uWalletBalance += amount
        # to_user.save(commit = False)

        from_user = CustomUser.objects.select_for_update().get(username=from_username)
        from_user.uWalletBalance -= amount
        from_user.uTransactionNumber += 1
        # from_user.save(commit = False)

        to_user.save()
        from_user.save()
        if email:
            OTP.verified_OTP(email, type)
    except Exception as e:
        return render (None, 'error_type1.html')


@transaction.atomic
def deposit(amount, to_username):
    try:
        to_user = CustomUser.objects.select_for_update().get(username=to_username)
        to_user.uWalletBalance += amount
        to_user.uTransactionNumber += 1
        to_user.save()
    except Exception as e:
        return render (None, 'error_type1.html')


@transaction.atomic
def withdraw(amount, from_username, new_role, new_plan):
    try:
        from_user = CustomUser.objects.select_for_update().get(username=from_username)
        if from_user.uWalletBalance >= amount:
            from_user.uWalletBalance -= amount
            from_user.uTransactionNumber += 1
            if new_role:
                from_user.role = new_role
                if new_role == 'premium':
                    from_user.premium_type = 'silver'
            if new_plan:
                from_user.premium_type = new_plan
            from_user.save()
            print('Done, amount', amount)
    except Exception as e:
        return render (None, 'error_type1.html')


@login_required
def make_transaction(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            form = TransactionForm(request.POST)

            if form.is_valid():
                try:
                    to_username = form.cleaned_data['to_username']
                    amount = form.cleaned_data['amount']

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

                        # print ("Hello, |" + to_username + "| Amount: ", amount)
                        if CustomUser.objects.exclude(username=request.user.username).filter(
                                username=to_username).exists():

                            from_username = request.user.username
                            otp_entered = request.POST.get("myText", None)
                            seekpassword = OTP.objects.filter(email=request.user.email).filter(mode=0)

                            if not otp_entered:
                                return HttpResponse("You have to enter OTP.")

                            if not seekpassword:
                                return HttpResponse("You have not generate OTP")

                            for var in seekpassword:
                                original_otp = var.onetimepassword
                                time_then = var.generationtime

                            utc = pytz.UTC
                            if int(otp_entered) == int(original_otp):
                                print("OTP Verified")
                                table_expired_datetime = time_then + timedelta(minutes=10)
                                time_now = datetime.now()

                                expired_on = table_expired_datetime.replace(tzinfo=utc)
                                checked_on = time_now.replace(tzinfo=utc)

                                if expired_on < checked_on:
                                    OTP.verified_OTP(request.user.email, 0)
                                    return HttpResponse(
                                        "OTP time expired. Please generate OTP again and then try again.")

                                else:
                                    exception = send_money(amount, to_username, from_username, request.user.email, 0)
                                    if exception:
                                        return HttpResponse(exception)
                                    form = form.save(commit=False)
                                    form.from_username = from_username
                                    print(form.from_username)
                                    form.save()
                                    return redirect('/')
                                    # return redirect(request, 'home.html', {'message':'Transaction successful'})
                            else:
                                print('OTP Incorrect')
                                # return render (None, 'error_type1.html')
                                return HttpResponse("OTP is Incorrect.")

                        else:
                            print("Username doesn't exists OR you have entered your own username.")
                            OTP.verified_OTP(request.user.email, 0)
                            return HttpResponse("Username doesn't exists")
                        # raise ValidationError(_("This email address is already in use. Please supply a different email address."))

                    else:
                        OTP.verified_OTP(request.user.email, 0)
                        return HttpResponse(
                            "Either you have not enough balance to process this request or you have exceeded your maximum transaction limit.")


                except Exception as e:
                    pass
                    OTP.verified_OTP(request.user.email, 0)
                    # print ("Error: ", e)
                    return render (None, 'error_type1.html')
                else:
                    pass

            return HttpResponse(request)

        else:
            form = TransactionForm
            return render(request, "index.html", {'form': form})

    else:
        return HttpResponse('You are not authenticated.')


@login_required
def upgrade_account(request):
    current_role = request.user.role
    username = request.user.username

    # user = CustomUser.objects.get(username = username)

    # if not user:
    # 	return HttpResponse('Technical problem has been occurred. Please try again.')

    amount = 1000
    new_role = current_role

    if current_role == 'casual':
        new_role = 'premium'
        amount = 1000
    elif current_role == 'premium':
        new_role = 'commercial'
        amount = 5000
        return render(request, 'upgrade.html')

    transaction_count = request.user.uTransactionNumber
    max_transactions_count = 99999
    if current_role == 'casual':
        max_transactions_count = 15
    elif current_role == 'premium':
        max_transactions_count = 30

    if request.user.uWalletBalance >= amount and transaction_count < max_transactions_count:
        withdraw(amount, username, new_role, None)
    else:
        return HttpResponse(
            'Either you do not have enough balance to upgrade your account or you cannot make this transaction because limit exceeded.')

    # return HttpResponse ('Your account has been upgraded')
    return redirect('/')


@login_required
def add_money_in_wallet(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddMoneyForm(request.POST)

            if form.is_valid():
                try:
                    amount = form.cleaned_data['amount']

                    if amount > 1000000:
                        return HttpResponse ("Please enter amount less than 1000000.")

                    if amount <= 0.0:
                        return HttpResponse("Amount should be greater than 0.")

                    transaction_count = request.user.uTransactionNumber
                    max_transactions_count = 99999
                    if request.user.role == 'casual':
                        max_transactions_count = 15
                    elif request.user.role == 'premium':
                        max_transactions_count = 30

                    if transaction_count < max_transactions_count:

                        from_username = request.user.username
                        otp_entered = request.POST.get("otp_field", None)
                        seekpassword = OTP.objects.filter(email=request.user.email).filter(mode=1)

                        if not otp_entered:
                            return HttpResponse("You have to enter OTP.")

                        if not seekpassword:
                            return HttpResponse("You have not generate OTP")

                        for var in seekpassword:
                            original_otp = var.onetimepassword
                            time_then = var.generationtime

                        utc = pytz.UTC
                        if int(otp_entered) == int(original_otp):
                            print("OTP Verified")
                            table_expired_datetime = time_then + timedelta(minutes=1)
                            time_now = datetime.now()

                            expired_on = table_expired_datetime.replace(tzinfo=utc)
                            checked_on = time_now.replace(tzinfo=utc)

                            if expired_on < checked_on:
                                OTP.verified_OTP(request.user.email, 1)
                                return HttpResponse("OTP time expired. Please generate OTP again and then try again.")

                            else:
                                OTP.verified_OTP(request.user.email, 1)
                                problem = deposit(amount, request.user.username)
                                if problem:
                                    return HttpResponse(problem)
                            return redirect('/')
                        else:
                            return HttpResponse('OTP Incorrect. Please try again.')
                            # return render (None, 'error_type1.html')
                    else:
                        return HttpResponse("Transaction limit exceeded to your account")
                except Exception as e:
                    return render (None, 'error_type1.html')
            else:
                return HttpResponse('Form is invalid')

        else:
            form = AddMoneyForm
            return render(request, "addmoney.html", {'form': form})
