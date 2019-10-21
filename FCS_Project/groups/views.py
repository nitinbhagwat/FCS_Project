from django.db.models import Subquery
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView

from django.contrib.auth.models import User

import Authentication
from Authentication.models import CustomUser

import friends
from friends.models import Friend

from groups.models import Group, Joined_group

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


@login_required(login_url="/users/login/")
def groups_view(request):
    if request.method == "POST":
        name_entered = request.POST.get("myText", None)
        price_entered = request.POST.get("priceText", None)
        create_group(request, name_entered, price_entered)

    group_display = Joined_group.objects.filter(member_name=request.user.username)
    group_display1 = Group.objects.exclude(group_name__in=Subquery(group_display.values('group_name'))).exclude(
        admin_name=request.user.username)

    recieved_requests = Group.objects.filter(admin_name=request.user.username)
    recieved_requests1 = Joined_group.objects.filter(
        group_name__in=Subquery(recieved_requests.values('group_name'))).filter(status=0)

    mygroups = Joined_group.objects.filter(member_name=request.user.username).filter(status=1)

    ownedgroups = Group.objects.filter(admin_name=request.user.username)

    extra_info = CustomUser.objects.filter(username=request.user.username)

    manage_info1 = Group.objects.filter(admin_name=request.user.username)
    manage_info = Joined_group.objects.filter(group_name__in=Subquery(manage_info1.values('group_name'))).filter(
        status=1)

    manage = CustomUser.objects.exclude(username=request.user.username)

    manage1 = Joined_group.objects.exclude(status=0)
    manage2 = Group.objects.filter(admin_name=request.user.username).exclude(group_name__in=Subquery(manage1.values('group_name')))

    # manage = CustomUser.objects.exclude(username__in=Subquery(manage_info.values('member_name'))).exclude(username=request.user.username)

    return render(request, 'groups/groups.html',
                  {'group_display1': group_display1, 'recieved_requests1': recieved_requests1, 'mygroups': mygroups,
                   'ownedgroups': ownedgroups, 'extra_info': extra_info, 'manage_info': manage_info, 'manage': manage, 'manage2': manage2})
filter

def create_group(request, name_entered, price_entered):
    list_groupnames = []
    list_admins = []

    var1 = Group.objects.all()

    var3 = CustomUser.objects.filter(username=request.user.username)

    for var2 in var1:
        list_groupnames.append(var2.group_name)

    if name_entered not in list_groupnames:
        for var4 in var3:
            if var4.role == 'casual':
                print('You are not authorized to create a group')

            else:
                Group.create(name_entered, request.user.username, price_entered)
    else:
        print('Your request cannot be processed')

    return redirect('/groups')


def group_operations(request, operation, variable, pk):
    store_group = ""

    if operation == 'join':
        Joined_group.join(request.user.username, pk)
        store_group = pk

    if operation == 'accept':
        Joined_group.accept(variable, pk)

    if operation == 'reject':
        Joined_group.reject(variable, pk)

    if operation == 'leave':
        Joined_group.leave(request.user.username, pk)

    if operation == 'delete':
        Joined_group.deletes(pk)
        Group.deletes(request.user.username, pk)

    if operation == 'deletemember':
        Joined_group.deletesmember(variable, pk)

    if operation == 'addmember':
        Joined_group.addmember(variable, pk)


    return redirect('/groups')
