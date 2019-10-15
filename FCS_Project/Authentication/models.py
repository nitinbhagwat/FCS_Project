from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
	pass
	# addictional fields here.
	username = models.CharField(max_length=20, primary_key = True)
	first_name = models.CharField(max_length=20, blank = False, null = False)
	last_name = models.CharField(max_length=20, blank = False, null = False)
	email = models.EmailField(_('email address'), unique=True)
	# 1 for Male, 0 for Female
	gender = models.BooleanField(default = True, blank = False, null = False)
	user_type = ( ('casual', 'Casual User'),
			   ('premium', 'Premium User'),
			   ('commercial', 'Commercial User'),
			   )
	role = models.CharField(max_length=20, choices = user_type, default = 'casual')
	age = models.IntegerField()
	contact = models.IntegerField(blank = False, null = False)
	uTransactionNumber = models.IntegerField(blank = True, null = True)
	uTimelinePrivacy = models.CharField(max_length=20, blank = True, null = True)
	uWalletBalance = models.FloatField(default = 500.00)
	# uPassword = models.CharField(max_length = 50)

	def __str__(self):
		return '{username}'