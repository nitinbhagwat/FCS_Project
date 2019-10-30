from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Announcement
from django.apps import apps
from django.db.models import Q

from .forms import CreateAnnouncementForm

# Create your views here.

@login_required
def create_announcement(request, group_name):
    # Check if it is a valid groups.
    GroupModel = apps.get_model('groups', 'Group')
    group_admin = ''
    try:
        group = GroupModel.objects.get(group_name=group_name)
        group_admin = group.admin_name
    except GroupModel.DoesNotExist:
        raise Http404("Group does not exist.")

    # Check if the requested user is the admin of group.
    if request.user.username != group_admin:
        raise Http404("You are not the admin of the Group.")

    if request.method == 'POST':
        form = CreateAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.group_name = group_name
            announcement.save()

    form = CreateAnnouncementForm()

    return render(request, 'create_announcement.html', {'form': form})


@login_required
def show_announcements(request, group_name):
    # Check if it is a valid groups.
    GroupModel = apps.get_model('groups', 'Group')
    try:
        group = GroupModel.objects.get(group_name=group_name)
    except GroupModel.DoesNotExist:
        raise Http404("Group does not exist.")

    # Check if the requested user is the admin or group member of the group.
    Joined_groupModel = apps.get_model('groups', 'Joined_group')
    try:
        is_group_admin = (GroupModel.objects.filter(Q(group_name=group_name, admin_name=request.user.username)).count() == 1)
        if not is_group_admin:
            joined_group = Joined_groupModel.objects.get(Q(group_name=group_name, member_name=request.user.username))
    except Joined_groupModel.DoesNotExist:
        raise Http404("You are not the member of this group.")

    announcements = []
    try:
        announcements = Announcement.objects.filter(group_name=group_name)
    except Announcement.DoesNotExist:
        print('Announcements belonging to this group does not exist.')

    return render(request, 'show_announcements.html', {'announcements':announcements})