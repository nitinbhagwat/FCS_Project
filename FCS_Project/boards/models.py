from django.db import models
from django import forms

class Users(models.Model):
	uId = models.IntegerField(max_length=10)
	uFirstName = models.CharField(max_length=20, blank = False, null = False)
	uLastName = models.CharField(max_length=20, blank = False, null = False)
	uEmail = models.EmailField(blank = False, null = False)
	uGender = models.BooleanField(default = True, blank = False, null = False)
	uRole = models.CharField(max_length=20)
	uDOB = models..DateField(input_formats=['%d/%m/%Y'])
	uContact = models.IntegerField(max_length=10, blank = False, null = False)
	uTransactionNumber = models.IntegerField(max_length=20, blank = False, null = False)
	uTimelinePrivacy = models.CharField(max_length=20, blank = False, null = False)
	uPassword = models.CharField(widget = forms.PasswordInput)


	class Meta:
		db_table = "Users"

