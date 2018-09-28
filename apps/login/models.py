from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def loginValidator(self, postData):
        errors ={}
        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        try:
            if len(postData['userName']) == 0 or len(postData['password']) == 0:
                errors['blank'] = "Must fill out all fields"
                return errors
            if len(postData['email']) == 0  or len(postData['fName']) == 0  or len(postData['lName']) == 0:
                errors['blank'] = "Must fill out all fields"
                return errors
            if len(postData['userName']) < 4:
                errors['userName'] = "Username is too short"
            if postData['password'] != postData['confPassword']:
                errors['password'] = 'Passwords do not match'
                return errors
            if bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', postData['password'])) == False:
                errors['password'] = 'Password must contain a number and a letter'
                return errors
            if len(postData['password']) < 7:
                errors['password'] = 'Password must be at least 8 characters'
                return errors
            if not emailRegEx.match(postData['email']):
                errors['email'] = 'Invalid email'
                return errors
            if postData == True:
                errors['database'] = 'Username or email already exists'
                return errors
        except:
            print("except: checking database")
            if postData['userName'] == "happy":
                errors['userName'] = 'Username or password incorrect'
                return errors
        return errors
    # def loggedIn(self, postData):
    #     validHash = User.objects.get(userName = postData['userName']).hashId
    #     if validHash != postData['hashId']:
    #         return False
    #     else:
    #         return True
        

        

class User(models.Model):
    userName = models.CharField(max_length=255)
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hId = models.CharField(max_length=255, default='abracadabraB')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    # place = models.OneToOneField(
    #     Place,
    #     on_delete=models.CASCADE,
    #     primary_key=True,
    # )