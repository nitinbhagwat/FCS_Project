from django.shortcuts import render, redirect
from Transactions.forms import TransactionForm
from django.http import HttpResponse
from django.forms import ValidationError
from Authentication.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db import transaction
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
							
							with transaction.atomic():
								to_user = CustomUser.objects.select_for_update().get(username = to_username)
								to_user.uWalletBalance += amount
								# to_user.save(commit = False)

								from_user = CustomUser.objects.select_for_update().get(username = from_username)
								from_user.uWalletBalance -= amount
								# from_user.save(commit = False)

								to_user.save()
								from_user.save()

							return redirect('/')
							
						else:
							print ("Username doesn't exists")
							return HttpResponse ("Username doesn't exists")
							#raise ValidationError(_("This email address is already in use. Please supply a different email address."))
					
					else:
						return HttpResponse ("Not enough balance to process this request.")


				except Exception as e:
					print ("Error: ", e)
					return HttpResponse(e)
				

			return HttpResponse(request)
		else:
			form  = TransactionForm
			return render (request, "index.html", {'form': form})

	else:
		pass
		# return redirect("/users/login")
	