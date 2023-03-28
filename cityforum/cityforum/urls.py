from django.contrib import admin
from django.urls import path
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('forum/<str:title>', views.forumView, name='forum'),
    path('forum/<str:title>/<slug:slug>', views.threadView, name='thread'),
]
