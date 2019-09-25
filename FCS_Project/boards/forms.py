from django import forms
from django.contrib.auth.decorators import login_required
from boards.models import Users

class UserForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = "uFirstName", "uLastName", "uEmail", "uContact", "uGender", "uRole", "uDOB", "uPassword" 
		# fields = "__all__" # to make form with all fields
		