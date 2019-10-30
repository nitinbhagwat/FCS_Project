from django.shortcuts import render, redirect
from django.http import HttpResponse
from Authentication.forms import ChangePremiumPlanForm, UserLoginForm
from Authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from time import sleep
# Create your views here.

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from Transactions.views import withdraw
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

@login_required
def change_premium_plan(request):
	if request.method == "POST":
		form = ChangePremiumPlanForm(request.POST)
		if form.is_valid():
			try:
				amount = 0
				current_plan = request.user.premium_type
				new_plan = form.cleaned_data['premium_type']
				if current_plan == new_plan:
					return HttpResponse ('You have not modified your plan.')
				if new_plan == 'silver' or current_plan == 'commercial' or (current_plan == 'gold' and new_plan == 'silver'):
					return HttpResponse ('You cannot downgrade your plan as per our user guide.')
				if new_plan == 'gold':
					amount = 100
				elif new_plan == 'platinum':
					amount = 150
				username = request.user.username
				balance = request.user.uWalletBalance
				if balance >= amount:
					exception = withdraw(amount, username, None, new_plan)
					if exception:
						print ('Error occured in group transaction')
						return HttpResponse(exception)
				else:
					return HttpResponse('You do not have enough balance to change your plan.')
				return redirect('/')
			except Exception as e:
				return HttpResponse(e)
		else:
			return HttpResponse('Form is not valid')
	else:
		form  = ChangePremiumPlanForm
		return render (request, "changepremiumplan.html", {'form': form})

def login_user(request):
	print (request.session.get('invalid_login_attempts'))
	if request.user.username:
		return HttpResponse ('You are already logged in. Please logout first if you want to login with different user.')

	if request.session.get('invalid_login_attempts') is None:
		request.session['invalid_login_attempts'] = 0
		
	elif request.session.get('invalid_login_attempts') == 3:
		print ('Sleeping ..')
		sleep(60)	
		request.session['invalid_login_attempts'] = 0
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		login_attempts = request.session.get('invalid_login_attempts', 0)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			temp_user = authenticate (username = username, password = password)
			request.session['invalid_login_attempts'] = login_attempts + 1
			login_attempts = request.session.get('invalid_login_attempts')
			if login_attempts <= 3:
				if temp_user is not None:
					login(request, temp_user)
					print ('login')
					request.session['invalid_login_attempts'] = 0
					return redirect ('/')
				else:
					form = UserLoginForm()
					return render(request, 'registration/login.html', {'message': 'Invalid Login Credentials. Please try again with correct credentials.', 'form': form})
		else:
			return render (None, 'error_type1.html')
	else:
		form = UserLoginForm()
	return render (request, 'registration/login.html', {'form': form})