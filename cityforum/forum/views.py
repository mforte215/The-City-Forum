from django.shortcuts import render, redirect
from .models import Forum, Thread
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def loginView(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['word']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('SUCCESS')
            return HttpResponseRedirect(reverse('index'))
        else:
            print('FAILURE')
            return render(request, 'registration/login.html', {})


def logoutView(request):
    logout(request)
    print('Running logout view')
    if request.user is not None:
        print("Something went wrong!")
    return redirect('login')