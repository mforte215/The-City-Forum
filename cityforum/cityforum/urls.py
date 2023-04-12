from django.contrib import admin
from django.urls import path
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('forum/<str:title>', views.forumView, name='forum'),
    path('forum/<str:title>/<slug:slug>', views.threadView, name='thread'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('sign-up/', views.signupView, name='sign-up'),
    path('add-thread/', views.AddThreadView, name='add-thread'),
    path('delete-comment/<slug:slug>', views.DeleteCommentView, name='delete-comment'),
    path('profile/', views.ProfileView, name='profile')
]
