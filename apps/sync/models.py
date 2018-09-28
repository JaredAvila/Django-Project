from __future__ import unicode_literals
from django.db import models
from apps.login.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=500)
    ingr = models.TextField(null=True)
    url = models.TextField(null=True)
    image = models.TextField(null=True)
    serves = models.IntegerField(null=True)
    user = models.ManyToManyField(User, related_name='userRecipes')
    love = models.ManyToManyField(User, related_name='lovedRecipes')

class Post(models.Model):
    post = models.TextField(1000, null=True)
    postUser = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    postRecipe = models.ForeignKey(Recipe, null=True, related_name='reicpePosts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField(1000, null=True)
    commentUser = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    commentPost = models.ForeignKey(Post, related_name='postComments', on_delete=models.CASCADE, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)