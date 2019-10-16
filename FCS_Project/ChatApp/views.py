from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Chat
from django.apps import apps
from django.db.models import Q

from .forms import ChatMessageForm


# Create your views here.
@login_required
def chat_function(request, user_name):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.from_user_name = request.user.username
            chat.to_user_name = user_name
            chat.chat_message = form.cleaned_data.get('message')
            chat.save()

    form = ChatMessageForm()

    chats = []
    try:
        chats = Chat.objects.filter(
            Q(from_user_name=request.user.username, to_user_name=user_name) |
            Q(from_user_name=user_name, to_user_name=request.user.username)
        )
    except Chat.DoesNotExist:
        print('Chat belonging to to_user_name Does not exist.')

    return render(request, 'chat_page.html', {'who': request.user.username, 'chats': chats, 'form': form})


@login_required
def chats_count_function(request, user_name):
    chat_objects_count = Chat.objects.filter(
            Q(from_user_name=request.user.username, to_user_name=user_name) |
            Q(from_user_name=user_name, to_user_name=request.user.username)
        ).count()
    data = {
        'count': chat_objects_count
    }
    return JsonResponse(data)