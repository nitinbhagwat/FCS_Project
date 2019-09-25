from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from boards.forms import UserForm
from boards.models import Users

# MY CONTROLLER

from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, World!')

def add_user(request):
	# if executes when we press submit button else not
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				return redirect("/show_details")
			except Exception as e:
				pass
	else:
		form = UserForm()

	return render(request, "index.html", {'form': form})


# login-required not working
@login_required
def show_details(request):
	users = Users.objects.all()
	return render (request, "show.html", {'users': users})
	
