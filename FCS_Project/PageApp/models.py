from django.db import models


# Create your models here.
class Page(models.Model):
    user_name = models.CharField(max_length=10)
    title = models.CharField(max_length=10)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)