from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField


class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    

    def __str__(self):
        return f"{self.title}"

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads', null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads', null=True, blank=False)
    body = models.TextField()
    slug = models.SlugField(unique=True, db_index=True, blank=True, max_length=255)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_comments', null=False)
    body = RichTextField()
    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"