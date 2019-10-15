from django.db import models

class Transactions(models.Model):
	from_username = models.CharField(max_length = 20)
	to_username = models.CharField(max_length = 20)
	amount = models.FloatField()
	created_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		db_table = "Transactions"