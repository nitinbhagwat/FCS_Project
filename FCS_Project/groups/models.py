from django.db import models


# Create your models here.

class Group(models.Model):
    gid = models.IntegerField(default="")
    group_name = models.CharField(max_length=20, default="", primary_key=True)
    admin_name = models.CharField(max_length=20, default="")
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "Group"
        unique_together = (("group_name", "admin_name"),)

    @classmethod
    def create(cls, name_entered, admin_name, price_entered):

        var2 = Group.objects.count()
        var2 = var2 + 1

        var1 = Group(var2, name_entered, admin_name, price_entered)

        try:
            var1.save()

        except:
            pass

    @classmethod
    def deletes(cls, admin_name, group_name):
        Group.objects.all().filter(group_name=group_name).filter(admin_name=admin_name).delete()


class Joined_group(models.Model):
    jid = models.IntegerField(default="")
    group_name = models.CharField(max_length=20, default="", primary_key=True)
    member_name = models.CharField(max_length=20, default="")
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "joined_Group"
        unique_together = (("group_name", "member_name"),)

    @classmethod
    def join(cls, member_name, group_name):
        var2 = Joined_group.objects.count()
        var2 = var2 + 1
        var1 = Joined_group(var2, group_name, member_name, 0)

        try:
            var1.save()
        except:
            pass

    @classmethod
    def accept(cls, group_name, member_name):
        Joined_group.objects.all().filter(member_name=member_name).filter(group_name=group_name).delete()
        var2 = Joined_group.objects.count()
        var2 = var2 + 1
        var1 = Joined_group(var2, group_name, member_name, 1)
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

