from django import forms
from .models import Comment, Thread
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        fields = ('body',)

class ThreadForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title-input'}))
    body = forms.CharField(widget=CKEditorWidget())
    
    labels = {
        'body': 'thread text',
    }


    class Meta:
        model = Thread
        fields = ('title','body',)