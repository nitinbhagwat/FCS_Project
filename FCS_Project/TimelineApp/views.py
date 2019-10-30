from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Post
from django.apps import apps
from django.db.models import Q

from .forms import PostMessageForm


# Create your views here.
@login_required
def timeline(request, to_user_name):
    # Valid sender is checked by the @login_required decorator.
    # Check If receiver is a valid user.
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    privacy = 'global'
    try:
        user = CustomUser.objects.get(username=to_user_name)
        privacy = user.uTimelinePrivacy
    except CustomUser.DoesNotExist:
        raise Http404("Receiver does not exist.")

    friendship_status = False
    if request.user.username != to_user_name:
        Friends = apps.get_model('friends', 'Friend')
        try:
            friendship = Friends.objects.get(Q(sendername=request.user.username, recievername=to_user_name))
            if friendship.status == 1:
                friendship_status = True
        except Friends.DoesNotExist:
            friendship_status = False

    # Implement privacy settings.
    if request.user.username != to_user_name and privacy == 'only me':
        raise Http404("Sender is not allowed to write or view Receiver's Timeline.")

    if request.user.username != to_user_name and friendship_status == False and privacy == 'friends':
        raise Http404('Sender is not the Friend of the Receiver.')

    if request.method == 'POST':
        # Check if the request is initiated from the owner or from its friends.
        # Because only owner of the account or its friend can post on the group.
        if request.user.username != to_user_name and friendship_status == False:
            raise Http404('Sender is not the Friend of the Receiver.')


        form = PostMessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.from_user_name = request.user.username
            post.to_user_name = to_user_name
            post.posted_message = form.cleaned_data.get('message')
            post.from_user_gender = request.user.gender
            post.save()

    form = PostMessageForm()

    posts = []
    try:
        posts = Post.objects.filter(to_user_name=to_user_name)
    except Post.DoesNotExist:
        print('Post belonging to to_user_name Does not exist.')

    return render(request, 'timeline.html', {'form': form, 'posts': posts})

@login_required
def latest_post(request, to_user_name):
    # Valid sender is checked by the @login_required decorator.
    # Check If receiver is a valid user.
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    privacy = 'global'
    try:
        user = CustomUser.objects.get(username=to_user_name)
        privacy = user.uTimelinePrivacy
    except CustomUser.DoesNotExist:
        raise Http404("Receiver does not exist.")

    friendship_status = False
    if request.user.username != to_user_name:
        Friends = apps.get_model('friends', 'Friend')
        try:
            friendship = Friends.objects.get(Q(sendername=request.user.username, recievername=to_user_name))
            if friendship.status == 1:
                friendship_status = True
        except Friends.DoesNotExist:
            friendship_status = False

    # Implement privacy settings.
    if request.user.username != to_user_name and privacy == 'only me':
        raise Http404("Sender is not allowed to write or view Receiver's Timeline.")

    if request.user.username != to_user_name and friendship_status == False and privacy == 'friends':
        raise Http404('Sender is not the Friend of the Receiver.')

    post_objects_count = Post.objects.filter(to_user_name=to_user_name).count()
    data = {
        'count' : post_objects_count
    }
    return JsonResponse(data)
