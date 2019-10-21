from django.shortcuts import render, redirect
from django.http import HttpResponse
from Authentication.forms import ChangePremiumPlanForm
from Authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
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