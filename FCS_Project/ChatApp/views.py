from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Chat
from django.apps import apps
from django.db.models import Q

from .forms import ChatMessageForm

import traceback
import logging


# Create your views here.
@login_required
def chat_function(request, user_name):
    # Valid sender is checked by the @login_required decorator.
    # Check If receiver is a valid user.
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    # User is not permitted chat himself.
    if request.user.username == user_name:
        raise Http404("User can't chat to himself.")

    friendship_status = False
    Friends = apps.get_model('friends', 'Friend')
    friend_list_of_sender = []
    try:
        friendship = Friends.objects.get(Q(sendername=request.user.username, recievername=user_name))
        friend_list_of_sender = Friends.objects.filter(Q(sendername=request.user.username, status=1))
        if friendship.status == 1:
            friendship_status = True
    except Friends.DoesNotExist:
        friendship_status = False


    if request.method == 'POST':
        # Casual user is not allowed to do send private message.
        if request.user.role == 'casual':
            raise Http404("Casual user is not permitted to chat.")

        if request.user.role == 'premium' and friendship_status == False:
            raise Http404("Premium user is permitted to chat only with its friends.")

        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.from_user_name = request.user.username
            chat.to_user_name = user_name
            chat.chat_message = form.cleaned_data.get('message')
            chat.save()

    form = ChatMessageForm()

    chats = []
    all_chats_from_sender = []
    all_chats_to_sender = []
    try:
        chats = Chat.objects.filter(
            Q(from_user_name=request.user.username, to_user_name=user_name) |
            Q(from_user_name=user_name, to_user_name=request.user.username)
        )

        all_chats_from_sender = Chat.objects.filter(Q(from_user_name=request.user.username))
        all_chats_to_sender = Chat.objects.filter(Q(to_user_name=request.user.username))
    except Chat.DoesNotExist:
        print('Chat belonging to to_user_name Does not exist.')

    # Populating the list of users.
    list_of_users_with_whom_requested_user_chats = set()
    for chat in all_chats_from_sender:
        list_of_users_with_whom_requested_user_chats.add(chat.to_user_name)
    for chat in all_chats_to_sender:
        list_of_users_with_whom_requested_user_chats.add(chat.from_user_name)
    for friend in friend_list_of_sender:
        list_of_users_with_whom_requested_user_chats.add(friend.recievername)

    if request.user.role == 'commercial':
        try:
            users = CustomUser.objects.all()
            for user in users:
                if user.username != request.user.username:
                    list_of_users_with_whom_requested_user_chats.add(user.username)
        except Exception as e:
            logging.error(traceback.format_exc())

    list_of_users_with_whom_requested_user_chats = list(list_of_users_with_whom_requested_user_chats)

    return render(request, 'chat_page.html', {'sender': request.user.username,
                                              'receiver': user_name,
                                              'chats': chats,
                                              'form': form,
                                              'chat_to_users':list_of_users_with_whom_requested_user_chats})


@login_required
def chats_count_function(request, user_name):
    # Valid sender is checked by the @login_required decorator.
    # Check If receiver is a valid user.
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    # User is not permitted chat himself.
    if request.user.username == user_name:
        raise Http404("User can't chat to himself.")


    chat_objects_count = Chat.objects.filter(
            Q(from_user_name=request.user.username, to_user_name=user_name) |
            Q(from_user_name=user_name, to_user_name=request.user.username)
        ).count()
    data = {
        'count': chat_objects_count
    }
    print(chat_objects_count)
    return JsonResponse(data)