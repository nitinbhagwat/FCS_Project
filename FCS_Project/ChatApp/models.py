from django.db import models


# Create your models here.
class Chat(models.Model):
    from_user_name = models.CharField(max_length=10)
    to_user_name = models.CharField(max_length=10)
    chat_message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
