import pyotp
from django.db import models
import Authentication

from Authentication.models import CustomUser


# Create your models here.


class Friend(models.Model):
    # objects = None
    id = models.AutoField(primary_key=True)
    sendername = models.CharField(max_length=20, default="")
    recievername = models.CharField(max_length=20, default="")
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "Friend"
        unique_together = (("sendername", "recievername"),)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        var2 = Friend.objects.count()
        var2 = var2 + 1
        var1 = Friend(var2, current_user, new_friend, 0)
        var2 = var2 + 1
        var3 = Friend(var2, new_friend, current_user, -1)
        try:
            var1.save()
            var3.save()
        except:
            pass

    @classmethod
    def loose_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()

    @classmethod
    def accept_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()
        var2 = Friend.objects.count()
        var2 = var2 + 1
        var1 = Friend(var2, current_user, new_friend, 1)
        var2 = var2 + 1
        var3 = Friend(var2, new_friend, current_user, 1)
        try:
            var1.save()
            var3.save()
        except:
            pass

    @classmethod
    def reject_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()


class Friend(models.Model):
    # objects = None
    id = models.AutoField(primary_key=True)
    sendername = models.CharField(max_length=20, default="")
    recievername = models.CharField(max_length=20, default="")
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "Friend"
        unique_together = (("sendername", "recievername"),)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        var2 = Friend.objects.count()
        var2 = var2 + 1
        var1 = Friend(var2, current_user, new_friend, 0)
        var2 = var2 + 1
        var3 = Friend(var2, new_friend, current_user, -1)
        try:
            var1.save()
            var3.save()
        except:
            pass

    @classmethod
    def loose_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()

    @classmethod
    def accept_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()
        var2 = Friend.objects.count()
        var2 = var2 + 1
        var1 = Friend(var2, current_user, new_friend, 1)
        var2 = var2 + 1
        var3 = Friend(var2, new_friend, current_user, 1)
        try:
            var1.save()
            var3.save()
        except:
            pass

    @classmethod
    def reject_friend(cls, current_user, new_friend):
        Friend.objects.all().filter(sendername=current_user).filter(recievername=new_friend).delete()
        Friend.objects.all().filter(sendername=new_friend).filter(recievername=current_user).delete()




