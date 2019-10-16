from django import forms

from .models import Page

class CreatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content']