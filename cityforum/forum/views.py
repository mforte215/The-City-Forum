from django.shortcuts import render, redirect
from .models import Forum, Thread
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
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

def signupView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/sign-up.html')
    if request.method == 'POST':
        username = request.POST['user']
        password1 = request.POST['word1']
        password2 = request.POST['word2']
        if username is not None:
            '''Try to see if this username is already taken'''
            existing_user = User.objects.get(username=username)
            if username is not None:
                return render(request, 'registration/sign-up.html')
            else:
                if password1 is not None:
                    if password1 == password2:
                        new_user = User(username=username, password=password1)
                        new_user.save()
                        login(request, new_user)
                        return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'registration/sign-up.html')
                
