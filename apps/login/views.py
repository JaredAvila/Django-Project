from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *

def login(request):
    return render(request, 'login/login.html')

def regi(request):
    return render(request, 'login/registration.html')

def loginValidation(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    loggedUser = User.objects.get(userName = request.POST['userName'])
    if not bcrypt.checkpw(request.POST['password'].encode(), loggedUser.password.encode()):
        messages.error(request, 'Password or username is incorrect')
        return redirect('/')
    else:
        request.session['userName'] = request.POST['userName']
        request.session['hId'] = loggedUser.hId
        request.session['id'] = loggedUser.id
        return redirect('/home')

def regiValidation(request):
    print('in regiValidation')
    errors = User.objects.loginValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regi')
    else:
        hashPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        hID = bcrypt.hashpw(request.POST['userName'].encode(), bcrypt.gensalt())
        newUser = User(userName = request.POST['userName'], fName = request.POST['fName'], lName = request.POST['lName'], email = request.POST['email'], password = hashPW, hId = hID)
        newUser.save()
        loggedUser = User.objects.get(userName = request.POST['userName'])
        request.session['hId'] = loggedUser.hId
        request.session['id'] = loggedUser.id
        request.session['userName'] = request.POST['userName']
        return redirect('/home')