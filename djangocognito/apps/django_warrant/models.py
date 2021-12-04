from django.contrib.auth.models import User
from django.db import models

class Token(models.Model):
    access_token = models.TextField()
    id_token = models.TextField()
    refresh_token = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)