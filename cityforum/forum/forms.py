from django import forms
from .models import Comment, Thread
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        labels = {
            "body": ""
        }
        fields = ('body',)



class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = [ 'forum','title','body',]
        labels = {
            "body": "",
            "title": "Thread Title"
        }
        widgets = {
            "title": forms.TextInput(attrs={'class': 'title-input'}),
        }