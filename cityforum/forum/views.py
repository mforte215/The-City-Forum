from django.shortcuts import render, redirect
from .models import Forum, Thread, Comment
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
        comments = Comment.objects.filter(thread=thread)
        return render(request, 'forum/thread.html', {'thread': thread, 'forum': forum, 'comments': comments})

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
            existing_user = User.objects.filter(username=username).exists()
            if existing_user:
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
                
def AddThreadView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            forums = Forum.objects.all()
            return render(request, 'forum/add-thread.html', {'forums': forums})
        else:
            return render(request, 'registration/login.html')
    if request.method == 'POST':
        if request.user.is_authenticated:
            thread_forum = request.POST['thread-forum']
            title = request.POST['title']
            body = request.POST['body']
            '''Needs to be forum instance so need to get forum object'''
            forum = Forum.objects.get(id=thread_forum)
            new_thread = Thread(forum=forum, title=title, body=body)
            new_thread.save()
            threads = Thread.objects.filter(forum__id=thread_forum)
            return render(request, 'forum/forum.html', {'threads': threads, 'forum': forum })
        else:
            return render(request, 'registration/login.html')    
