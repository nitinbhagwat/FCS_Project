from django.db import models


# Create your models here.
class Post(models.Model):
    from_user_name = models.CharField(max_length=10)
    to_user_name = models.CharField(max_length=10)
    posted_message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    from_user_gender = models.BooleanField(default = True, blank = False, null = False)