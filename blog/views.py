from django.shortcuts import render
from django.http import HttpResponse

from . import models

# Create your views here.
def index(request):
    posts = models.Post.objects.all()
    return render(request, 'blog/index.html', dict(posts=posts))

'''
def entry(request, entry_id):
    post = get_object_or_404(Post, pk=entry_id)
    return render(request, 'blog/entry.html', dict(post=post))
'''
