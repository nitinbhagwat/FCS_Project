from django.db import models

class User(models.Model):
	uid = models.CharField(max_length=10)
	uname = models.CharField(max_length=20)
	uemail = models.EmailField()
	ucontact = models.CharField(max_length=15)

	class Meta:
		db_table = "user"

