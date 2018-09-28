from __future__ import unicode_literals
from django.db import models
from apps.login.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    userItem = models.ForeignKey(User, related_name='userItems', on_delete=models.CASCADE)

class Checked(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    userChecked = models.ForeignKey(User, related_name='checkedItems', on_delete=models.CASCADE)