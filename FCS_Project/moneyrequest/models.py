import pyotp
from django.db import models
import Authentication
#
# import time
# import datetime
from datetime import datetime, time, timedelta
import pytz

from Authentication.models import CustomUser


# Create your models here.

class MoneyRequest(models.Model):
    # objects = None
    id = models.AutoField(primary_key=True)
    sendername = models.CharField(max_length=20, default="")
    recievername = models.CharField(max_length=20, default="")
    amount = models.FloatField(default="")
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "MoneyRequest"
        unique_together = (("sendername", "recievername"),)

    @classmethod
    def send(cls, current_user, friend_name, amount):

        var2 = MoneyRequest.objects.count()
        var2 = var2 + 1
        var1 = MoneyRequest(var2, current_user, friend_name, amount, 0)

        try:
            var1.save()
        except:
            pass

    @classmethod
    def accept(cls, current_user, friend_name):
        MoneyRequest.objects.all().filter(sendername=friend_name).filter(recievername=current_user).delete()


    @classmethod
    def reject(cls, current_user, friend_name):
        MoneyRequest.objects.all().filter(sendername=friend_name).filter(recievername=current_user).delete()
