from django import forms

from .models import Chat


class ChatMessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class' : 'chat-input'}), max_length=100, label="")

    class Meta:
        model = Chat
        fields = ['message']