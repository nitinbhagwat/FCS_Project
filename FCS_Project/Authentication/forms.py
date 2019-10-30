from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ["username", "first_name", "last_name", "email", "gender", "age", "uTimelinePrivacy"]
		# fields = "__all__" # to make form with all fields


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('username', 'email')

class ChangePremiumPlanForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = 'premium_type', 
			
		
class UserLoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=50)
		