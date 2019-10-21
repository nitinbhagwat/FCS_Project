from django import forms
from django.contrib.auth.decorators import login_required
from Transactions.models import Transactions

# class FetchUsername(forms.ModelForm):
# 	class Meta:
# 		model = Transactions
# 		fields = 'to_username',


class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = "to_username", "amount"
		# fields = "__all__" # to make form with all fields

class AddMoneyForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ("amount", )
			
		

# class OTPForm(forms.ModelForm):
# 	class Meta:
# 		model = OTP
# 		fields = 
			
			
			