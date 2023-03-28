from django.shortcuts import render
from .models import Forum, Thread

def index(request):
    if request.method == 'GET':
        forums = Forum.objects.all()
        latest_threads = Thread.objects.all().order_by('-id')[:10]
        return render(request, 'forum/index.html', {'forums': forums, 'latest_threads': latest_threads})
    
def forumView(request, title):
    if request.method == 'GET':
        forum = Forum.objects.get(title=title)
        threads = Thread.objects.filter(forum__title=title)
        return render(request, 'forum/forum.html', {'threads': threads, 'forum': forum })

def threadView(request, title, slug):
    if request.method == 'GET':
        forum = Forum.objects.get(title=title)
        thread = Thread.objects.get(slug=slug)
        return render(request, 'forum/thread.html', {'thread': thread, 'forum': forum })