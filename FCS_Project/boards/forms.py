from django import forms
from boards.models import User

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		# fields = "uid, uname, uemail, ucontact"
		fields = "__all__" # to make form with all fields
		
			
			
			

