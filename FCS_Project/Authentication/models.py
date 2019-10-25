from django.db import models
import pyotp
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
# Create your models here.

class CustomUser(AbstractUser):
	pass
	# addictional fields here.
	username = models.CharField(max_length=20, primary_key = True)
	first_name = models.CharField(max_length=20, blank = False, null = False)
	last_name = models.CharField(max_length=20, blank = False, null = False)
	email = models.EmailField(_('email address'), unique=True)
	# 1 for Male, 0 for Female
	gender_choice = ( (True, 'Male'), (False, 'Female'), )
	gender = models.BooleanField(default = True, blank = False, null = False, choices = gender_choice)
	user_type = ( ('casual', 'Casual User'),
			   ('premium', 'Premium User'),
			   ('commercial', 'Commercial User'),
			   )
	role = models.CharField(max_length=20, choices = user_type, default = 'casual')
	age = models.IntegerField()
	contact = models.IntegerField(blank = True, null = True)
	# Its a transaction count
	uTransactionNumber = models.IntegerField(blank = True, null = True, default = 0)
	uTimelinePrivacy = models.CharField(max_length=20, blank = True, null = True)
	uWalletBalance = models.FloatField(default = 500.00)
	premium_choices = (('silver', 'Silver'),
						('gold', 'Gold'),
						('platinum', 'Platinum'))
	premium_type = models.CharField(max_length = 10, choices = premium_choices, default='silver', blank = True, null = True)
	# uPassword = models.CharField(max_length = 50)

	def __str__(self):
		return '{username}'


class OTP(models.Model):
	
	email = models.EmailField(default="")
	status = models.IntegerField(default=0)
	onetimepassword = models.IntegerField(default="", primary_key = True)
	generationtime = models.DateTimeField(default = "")
	mode = models.IntegerField(default="")

	class Meta:
		unique_together = (("email", "mode"),)

	@classmethod
	def generate_OTP(cls, current_user_email, mode):

		totp = pyotp.TOTP('base32secret3232')
		password = totp.now()

		varid = OTP.objects.count()
		varid = varid+1
		time_now = datetime.now()
		varA = OTP(current_user_email, 0, password, time_now, mode)
		try:
			varA.save()
		except:
			pass

	@classmethod
	def verified_OTP(cls, current_user_email, type):
		OTP.objects.all().filter(email=current_user_email).filter(mode=type).delete()