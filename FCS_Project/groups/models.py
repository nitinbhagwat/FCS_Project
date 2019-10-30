from django.db import models
from django.http import HttpResponse

from Transactions.views import send_money


# Create your models here.

# 0 = closed group
# 1 = opened group

class Group(models.Model):
    group_name = models.CharField(max_length=20, default="", primary_key=True)
    admin_name = models.CharField(max_length=20, default="")
    price = models.IntegerField(default=0)
    type = models.IntegerField(default="")

    class Meta:
        db_table = "Group"
        unique_together = (("group_name", "admin_name"),)

    @classmethod
    def create(cls, name_entered, admin_name, price_entered, type):

        var1 = Group(name_entered, admin_name, price_entered, type)

        try:
            var1.save()

        except:
            pass

    @classmethod
    def deletes(cls, admin_name, group_name):
        Group.objects.all().filter(group_name=group_name).filter(admin_name=admin_name).delete()


class Joined_group(models.Model):
    firstfield = models.CharField(max_length=50, default="", primary_key=True)
    group_name = models.CharField(max_length=20, default="")
    member_name = models.CharField(max_length=20, default="")
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "joined_Group"
        unique_together = (("group_name", "member_name"),)

    @classmethod
    def join(cls, member_name, group_name):
        vara = member_name
        varb = group_name

        var1 = Joined_group(vara+varb, group_name, member_name, 0)

        try:
            var1.save()
        except:
            pass

    @classmethod
    def accept(cls, group_name, member_name):
        Joined_group.objects.all().filter(member_name=member_name).filter(group_name=group_name).delete()

        info = Group.objects.filter(group_name = group_name)
        amount = 0
        to_username = ""
        for var in info:
            amount = var.price
            to_username = var.admin_name
        from_username = member_name

        exception = send_money (amount, to_username, from_username, None, None)
        if exception:
            return HttpResponse (exception)

        vara = member_name
        varb = group_name

        var1 = Joined_group(vara+varb, group_name, member_name, 1)
        try:
            var1.save()
        except:
            pass

    @classmethod
    def reject(cls, group_name, member_name):
        Joined_group.objects.all().filter(member_name=member_name).filter(group_name=group_name).delete()


    @classmethod
    def leave(cls, member_name, group_name):
        Joined_group.objects.all().filter(member_name=member_name).filter(group_name=group_name).delete()

    @classmethod
    def deletes(cls, group_name):
        Joined_group.objects.all().filter(group_name=group_name).delete()

    @classmethod
    def deletesmember(cls, group_name, member_name):
        Joined_group.objects.all().filter(group_name=group_name).filter(member_name=member_name).delete()

    @classmethod
    def addmember(cls, group_name, member_name):
        Joined_group.objects.all().filter(group_name=group_name).filter(member_name=member_name).delete()

        vara = member_name
        varb = group_name

        var1 = Joined_group(vara+varb, group_name, member_name, 1)
        try:
            var1.save()
        except:
            pass
