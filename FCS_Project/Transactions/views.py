from django.shortcuts import render, redirect
from Transactions.forms import TransactionForm
from django.http import HttpResponse
from django.forms import ValidationError
from Authentication.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db import transaction
from Authentication.models import OTP
from django.core.mail import send_mail
from django.conf import settings

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


def verify_otp(request):
	OTP.generate_OTP(request.user.email)
	Func_sendmail(request, request.user.email)
	return redirect('/transactions')

def Func_otp(otp_entered, original_otp, email):
    if otp_entered == original_otp:
        print('CORRECT')
        OTP.verified_OTP(email)
    else:
        print('Incorrect......')
        return HttpResponse ("OTP is not verified.")


def Func_sendmail(request, rec_id):
    seekpassword1 = OTP.objects.filter(email=request.user.email)

    for var1 in seekpassword1:
        send_otp = var1.onetimepassword

    subject = 'Verification OTP'
    # str1 = 'Your OTP for verification is below. Donot share with anyone '
    # str2 = send_otp
    # str1.join(str2)

    message = str(send_otp)
    from_email = settings.EMAIL_HOST_USER
    to_list = [request.user.email]

    print(message)
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    # send_mail(subject, message, from_email, to_email, fail_silently= True)
	

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
						return HttpResponse ("Amount should be greater than 0.")

					wallet_balance = request.user.uWalletBalance

					if wallet_balance >= amount:
						
						# print ("Hello, |" + to_username + "| Amount: ", amount)
						if CustomUser.objects.exclude(username = request.user.username).filter(username = to_username).exists():
							
							from_username = request.user.username
							otp_entered = request.POST.get("myText", None)
							seekpassword = OTP.objects.filter(email=request.user.email)

							if not otp_entered:
								print ("User has not entered OTP")
								return HttpResponse ("You have to enter OTP.")

							if not seekpassword:
								print ("You have not generate OTP")
								return HttpResponse ("You have not generate OTP")


							for var in seekpassword:
								original_otp = var.onetimepassword
							
							# print("|", otp_entered, "|\n|", original_password, "|")
							# print (type(otp_entered))
							# print (type(original_otp))

							# Func_otp(int(otp_entered), int(original_password), request.user.email)

							if int(otp_entered) == int(original_otp):
								print ("OTP Verified")
								with transaction.atomic():
									to_user = CustomUser.objects.select_for_update().get(username = to_username)
									to_user.uWalletBalance += amount
									# to_user.save(commit = False)

									from_user = CustomUser.objects.select_for_update().get(username = from_username)
									from_user.uWalletBalance -= amount
									# from_user.save(commit = False)

									to_user.save()
									from_user.save()
									OTP.verified_OTP(request.user.email)

								return redirect('/')
							else:
								print ('OTP Incorrect')
								return HttpResponse ("OTP is not verified.")
							
						else:
							print ("Username doesn't exists OR you have entered your own username.")
							return HttpResponse ("Username doesn't exists")
							#raise ValidationError(_("This email address is already in use. Please supply a different email address."))
					
					else:
						return HttpResponse ("Not enough balance to process this request.")


				except Exception as e:
					pass
					# print ("Error: ", e)
					return HttpResponse(e)
				



		        

			return HttpResponse(request)

		else:
			form  = TransactionForm
			return render (request, "index.html", {'form': form})

	else:
		pass
		# return redirect("/users/login")
	