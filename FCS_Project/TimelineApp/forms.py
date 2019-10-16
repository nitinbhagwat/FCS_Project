from django import forms

from .models import Post

class PostMessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}), max_length=100, label="Create Post")

    class Meta:
        model = Post
        fields = ['message']