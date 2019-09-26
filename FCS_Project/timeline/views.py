from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
from django.http import JsonResponse
from timeline.models import Post


# Create your views here.
def hello(request):
    return HttpResponse(loader.get_template('timeline.html').render())

def store(request):
    #https://youtu.be/HSONRg33BBc
    msg = request.GET.get('msg', None)
    post_obj = Post(post=msg)
    post_obj.save()
    post_list_obj = Post.objects.all()
    post_list = ''
    for post in post_list_obj:
        post_list += post.post
    data = {
        'post_list': post_list
    }
    #Post.objects.all().delete() # https://stackoverflow.com/questions/4532681/how-to-remove-all-of-the-data-in-a-table-using-django
    return JsonResponse(data)
