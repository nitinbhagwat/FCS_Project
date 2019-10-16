from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# For models.
from .models import Page
from django.apps import apps

from .forms import CreatePageForm


# Create your views here.
@login_required
def create_page(request):
    CustomUser = apps.get_model('Authentication', 'CustomUser')
    try:
        user = CustomUser.objects.get(username=request.user.username)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

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
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

    pages = []
    try:
        pages = Page.objects.filter(user_name=user_name)
    except Page.DoesNotExist:
        print('Post belonging to to_user_name Does not exist.')

    return render(request, 'show_pages.html', {'pages':pages})