from django import forms

from .models import Announcement


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']