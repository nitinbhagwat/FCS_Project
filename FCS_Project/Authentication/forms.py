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
	class Meta(object):
		model = CustomUser
		fields = ('username', 'email')

class ChangePremiumPlanForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = 'premium_type', 
			
		
