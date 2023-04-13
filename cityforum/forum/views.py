from django.shortcuts import render, redirect
from .models import Forum, Thread, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, ThreadForm


def index(request):
    if request.method == 'GET':
        forums = Forum.objects.all()
        thread_list = Thread.objects.all().order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(thread_list, 10)

        try:
            threads = paginator.page(page)
        except PageNotAnInteger:
            threads = paginator.page(1)
        except EmptyPage:
            threads = paginator.page(page.num_pages)
        return render(request, 'forum/index.html', {'forums': forums, 'latest_threads': threads})
    
def forumView(request, title):
    if request.method == 'GET':
        forum = Forum.objects.get(title=title)
        thread_list = Thread.objects.filter(forum__title=title).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(thread_list, 10)

        try:
            threads = paginator.page(page)
        except PageNotAnInteger:
            threads = paginator.page(1)
        except EmptyPage:
            threads = paginator.page(page.num_pages)

        return render(request, 'forum/forum.html', {'threads': threads, 'forum': forum })

def threadView(request, title, slug):
    if request.method == 'GET':
        forum = Forum.objects.get(title=title)
        print('PRINTING FOUND FORUM IN GET')
        print(forum)
        thread = Thread.objects.get(slug=slug)
        comment_list = Comment.objects.filter(thread=thread).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(comment_list, 10)
        new_comment_form = CommentForm()
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(page.num_pages)
        
        return render(request, 'forum/thread.html', {'new_comment_form': new_comment_form, 'thread': thread, 'forum': forum, 'comments': comments})
    
    if request.method == 'POST':
        print('PRINTING POST REQUEST')
        print(request.POST)
        body = request.POST['body']
        if body:
            author = request.user
            thread = Thread.objects.get(slug=slug)
            new_comment = Comment(body=body, author=author, thread=thread)
            new_comment.save()
            new_comment_form = CommentForm()
            forum = Forum.objects.get(title=title)
            print('PRINTING FOUND FORUM IN POST REQUEST')
            print(forum)
            comment_list = Comment.objects.filter(thread=thread).order_by('-created_at')
            page = request.GET.get('page', 1)
            paginator = Paginator(comment_list, 10)
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                comments = paginator.page(1)
            except EmptyPage:
                comments = paginator.page(page.num_pages)
            return render(request, 'forum/thread.html', {'new_comment_form': new_comment_form, 'thread': thread, 'forum': forum, 'comments': comments})
        else:
            forum = Forum.objects.get(title=title)
            new_comment_form = CommentForm()
            thread = Thread.objects.get(slug=slug)
            comments = Comment.objects.filter(thread=thread).order_by('created_at')
            return render(request, 'forum/thread.html', {'new_comment_form': new_comment_form, 'thread': thread, 'forum': forum, 'comments': comments})

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
                        new_user = User(username=username)
                        new_user.set_password(password1)
                        new_user.save()
                        login(request, new_user)
                        return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'registration/sign-up.html')
                
def AddThreadView(request, forum=None):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print('NAVIGATED FORUM')
            print(forum)
            forums = Forum.objects.all()
            if forum is not None:
                forum_object = Forum.objects.get(title=forum)
                thread_form = ThreadForm(initial={'forum': forum_object})
                return render(request, 'forum/add-thread.html', {'forums': forums, 'thread_form': thread_form, 'active_forum': forum})
            else:
                thread_form = ThreadForm()
                return render(request, 'forum/add-thread.html', {'forums': forums, 'thread_form': thread_form, 'active_forum': forum})
        else:
            return render(request, 'registration/login.html')
    if request.method == 'POST':
        if request.user.is_authenticated:
            thread_forum = request.POST['forum']
            title = request.POST['title']
            body = request.POST['body']
            '''Needs to be forum instance so need to get forum object'''
            forum = Forum.objects.get(id=thread_forum)
            new_thread = Thread(forum=forum, title=title, body=body, author=request.user)
            new_thread.save()
            threads = Thread.objects.filter(forum__id=thread_forum).order_by('-created_at')
            return render(request, 'forum/forum.html', {'threads': threads, 'forum': forum })
        else:
            return render(request, 'registration/login.html')

def DeleteCommentView(request, slug):
    if slug:
        found_comment = Comment.objects.get(slug=slug)
        thread = found_comment.thread
        forum = thread.forum
        found_comment.delete()
        comment_list = Comment.objects.filter(thread=thread).order_by('created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(comment_list, 10)
        new_comment_form = CommentForm()
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(page.num_pages)
        
        return HttpResponseRedirect(reverse('thread', kwargs={'title': forum.title, 'slug': thread.slug}))

    else:
        return reverse('index')

def ProfileView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            '''Get user's threads'''
            user = request.user
            threads = Thread.objects.filter(author=user)
            '''Get user's comments'''
            comments = Comment.objects.filter(author=user)
            
            return render(request, 'forum/profile.html', {'threads': threads, 'comments': comments})
        else:
            return HttpResponseRedirect(reverse('login'))

def DeleteThreadView(request, slug):
    if slug:
        found_thread = Thread.objects.get(slug=slug)
        found_thread.delete()
        return HttpResponseRedirect(reverse('profile'))
    else:
        return HttpResponseRedirect(reverse('index'))