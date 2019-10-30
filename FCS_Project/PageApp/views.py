from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Page
from django.apps import apps
from django.db.models import Q

from .forms import CreatePageForm


# Create your views here.
@login_required
def create_page(request):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=request.user.username)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    if request.user.role != 'commercial':
        raise Http404("You are not a commercial user.")

    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.user_name = request.user.username
            page.save()

    form = CreatePageForm()

    return render(request, 'create_page.html', {'form': form})


@login_required
def show_pages(request, user_name):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=user_name)
        if user.role != 'commercial':
            raise Http404("User for which you are looking for is not a commercial user.")
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    pages = []
    try:
        pages = Page.objects.filter(user_name=user_name)
    except Page.DoesNotExist:
        print('Post belonging to to_user_name Does not exist.')

    return render(request, 'show_pages.html', {'pages':pages})

@login_required
def show_commercial_user(request):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    users = None
    try:
        users = CustomUser.objects.filter(Q(role='commercial'))
    except:
        raise Http404("Excpetion Occured.")

    commercial_users_name = []
    for user in users:
        commercial_users_name.append(user.username)

    count = len(commercial_users_name)

    return render(request, 'show_commercial_users.html', {'commercial_users_name':commercial_users_name, 'count': count})