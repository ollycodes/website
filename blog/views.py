from django.shortcuts import render
from django.http import HttpResponse

from . import models

# Create your views here.
def index(request):
    posts = models.Post.objects.all()
    return render(request, 'blog/index.html', dict(posts=posts))


