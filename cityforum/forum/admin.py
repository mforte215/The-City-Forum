from django.contrib import admin
from .models import Thread, Forum, Comment

admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Comment)