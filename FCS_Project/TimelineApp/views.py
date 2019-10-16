from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Post
from django.apps import apps

from .forms import PostMessageForm


# Create your views here.
@login_required
def timeline(request, to_user_name):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=to_user_name)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    if request.method == 'POST':
        form = PostMessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.from_user_name = request.user.username
            post.to_user_name = to_user_name
            post.posted_message = form.cleaned_data.get('message')
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
    post_objects_count = Post.objects.filter(to_user_name=to_user_name).count()
    data = {
        'count' : post_objects_count
    }
    return JsonResponse(data)
