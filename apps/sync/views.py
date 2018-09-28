from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import requests
import json
import re
from django.http import HttpResponseRedirect
import bcrypt
from .models import *
from apps.login.models import User
from apps.shopList.models import Item, Checked

def home(request):
    items = Item.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'sync/sync.html', {"items": items, "posts": posts})

def logout(request):
    request.session['userName'] = ''
    request.session['hId'] = ''
    return redirect('/')

def getRecipe(request):
    recipeData = requests.get('https://api.edamam.com/search?q=' + request.POST["item1"] + '+' + request.POST["item2"] + '+' + request.POST["item3"] + '&app_id=c804c269&app_key=ad79d88a2a8b07be1a581c0c79218223%20&from=0&to=10').json()
    request.session['recipeData'] = recipeData
    return redirect('/home/foundRecipe')

def foundRecipe(request):
    recipeNames = []
    recipeImages = []
    recipeUrls = []
    recipeIngrs = []
    recipeServes = []
    try:
        for i in range(5):
            recipeNames.append(request.session['recipeData']['hits'][i]['recipe']['label'])
            recipeImages.append(request.session['recipeData']['hits'][i]['recipe']['image'])
            recipeUrls.append(request.session['recipeData']['hits'][i]['recipe']['url'])
            recipeIngrs.append(request.session['recipeData']['hits'][i]['recipe']['ingredientLines'])
            recipeServes.append(request.session['recipeData']['hits'][i]['recipe']['yield'])
        print(recipeImages)
    except:
        errors= {}
        errors['blank'] = "***Error#401: Search returned no results.***"
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home')
    request.session['names'] = recipeNames
    request.session['images'] = recipeImages
    request.session['urls'] = recipeUrls
    request.session['ingrs'] = recipeIngrs
    request.session['serves'] = recipeServes
    request.session['currentNum'] = 0
    request.session['currentName'] = request.session['names'][0]
    request.session['currentImage'] = request.session['images'][0]
    request.session['currentUrl'] = request.session['urls'][0]
    request.session['currentIngr'] = request.session['ingrs'][0]
    request.session['currentServe'] = int(request.session['serves'][0])
    return render(request, 'sync/results.html')

def nextRecipe(request):
    request.session['currentNum'] += 1
    x = request.session['currentNum']
    request.session['currentName'] = request.session['names'][x]
    request.session['currentImage'] = request.session['images'][x]
    request.session['currentUrl'] = request.session['urls'][x]
    request.session['currentIngr'] = request.session['ingrs'][x]
    request.session['currentServe'] = int(request.session['serves'][x])
    return render(request, 'sync/recipe.html')

def prevRecipe(request):
    request.session['currentNum'] -= 1
    x = request.session['currentNum']
    request.session['currentName'] = request.session['names'][x]
    request.session['currentImage'] = request.session['images'][x]
    request.session['currentUrl'] = request.session['urls'][x]
    request.session['currentIngr'] = request.session['ingrs'][x]
    request.session['currentServe'] = int(request.session['serves'][x])
    return render(request, 'sync/recipe.html')

def addRecipe(request):
    recipes = Recipe.objects.all().values()
    user = User.objects.get(hId=request.session['hId'])
    for i in range(recipes.count()):
        if request.POST['name'] == recipes[i]['name']:
            new = Recipe.objects.get(name=request.POST['name'])
            new.user.add(user)
            errors= {}
            errors['blank'] = "*Recipe has been added to your box!*"
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
            return render(request, 'sync/recipe.html')
    ingrs = json.dumps(request.POST['ingr'])
    new = Recipe(name=request.POST['name'], ingr=ingrs, url=request.POST['url'], serves=int(request.POST['serve']), image=request.POST['image'])
    new.save()
    new.user.add(user)
    errors= {}
    errors['blank'] = "*Recipe has been added to your box!*"
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    return render(request, 'sync/recipe.html')

def recipeBox(request):
    user = User.objects.get(hId = request.session['hId'])
    return render(request, 'sync/recipeBox.html', {"recipes": Recipe.objects.filter(user = user)})

def viewRecipe(request, id):
    x = Recipe.objects.get(id=id)
    try:
        jsonDec = json.decoder.JSONDecoder()
        newLst = jsonDec.decode(x.ingr).split("'")[1:-1]
        newerLst = []
        for item in newLst:
            if item != ', ':
                newerLst.append(item)
        request.session['viewIngrs'] = newerLst
        request.session['viewUrl'] = x.url
        request.session['viewDirc'] = ''
    except:
        request.session['viewIngrs'] = x.ingr.split(',')
        request.session['viewDirc'] = x.url.split('.')
        request.session['viewUrl'] = '#'
    
    request.session['viewName'] = x.name
    request.session['viewServes'] = x.serves
    request.session['viewImage'] = x.image
    request.session['viewId'] = x.id
    
    return render(request, 'sync/viewRecipe.html')

def removeRecipe(request, id):
    recipe = Recipe.objects.get(id=id)
    user = User.objects.get(hId=request.session['hId'])
    recipe.user.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editRecipe(request, id):
    x = Recipe.objects.get(id=id)
    jsonDec = json.decoder.JSONDecoder()
    newLst = jsonDec.decode(x.ingr).split("'")[1:-1]
    newerLst = []
    for item in newLst:
        if item != ', ':
            newerLst.append(item)
    request.session['editIngrs'] = newerLst
    request.session['editName'] = x.name
    request.session['editServes'] = x.serves
    request.session['editImage'] = x.image
    request.session['editUrl'] = x.url
    return render(request, 'sync/editRecipe.html')

def createRecipe(request):
    items = Item.objects.all()
    return render(request, 'sync/createRecipe.html', {"items": items})

def creation(request):
    user = User.objects.get(hId=request.session['hId'])
    new = Recipe(name=request.POST['name'], serves=request.POST['serves'], url=request.POST['url'], ingr=request.POST['ingr'], image=request.POST['image'])
    new.save()
    new.user.add(user)
    return redirect('/home/recipeBox')

def viewProfile(request, id):
    items = Item.objects.all()
    user = User.objects.get(id=id)
    request.session['profilefName'] = user.fName
    request.session['profilelName'] = user.lName
    request.session['profileEmail'] = user.email
    return render(request, 'sync/profile.html', {"items": items})

def editProfile(request, id):
    items = Item.objects.all()
    user = User.objects.get(id=id)
    request.session['profilefName'] = user.fName
    request.session['profilelName'] = user.lName
    request.session['profileEmail'] = user.email
    return render(request, 'sync/editProfile.html', {"items": items})

def wallPost(request):
    print(request.POST['post'])
    try:
        print('in tyr')
        recipe = Recipe.objects.get(id=request.POST['id'])
        user = User.objects.get(hId=request.session['hId'])
        post = Post(post=request.POST['post'], postRecipe=recipe, postUser=user)
        post.save()
    except:
        print('in except')
        user = User.objects.get(hId=request.session['hId'])
        post = Post(post=request.POST['post'], postUser=user)
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def updateUser(request, id):
    try:
        errors={}
        if request.POST['new'] != request.POST['new-conf']:
            errors['error'] = 'New password and confirm password do not match'
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))           
        user = User.objects.get(hId = request.session['hId'])
        hashPW = bcrypt.hashpw(request.POST['new'].encode(), bcrypt.gensalt())
        user.password = hashPW
        user.save()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        user = User.objects.get(hId = request.session['hId'])
        user.userName = request.POST['userName']
        user.fName = request.POST['fName']
        user.lName = request.POST['lName']
        user.email = request.POST['email']
        user.save()
        request.session['userName'] = user.userName
    return redirect('/home')

def deletePost(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addRecipeFromView(request, id):
    new = Recipe.objects.get(id = id)
    user = User.objects.get(hId=request.session['hId'])
    new.user.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    request.session['userName'] = ''
    request.session['hId'] = ''
    request.session['profileEmail'] = ''
    request.session['profilelName'] = ''
    request.session['profilefName'] = ''
    request.session['editUrl'] = ''
    request.session['editImage'] = ''
    request.session['editServes'] = ''
    request.session['editIngrs'] = ''
    request.session['viewImage'] = ''
    request.session['viewIngrs'] = ''
    request.session['viewDirc'] = ''
    request.session['viewUrl'] = ''
    request.session['viewName'] = ''
    request.session['viewServes'] = ''
    request.session['currentName'] = ''
    request.session['currentImage'] = ''
    request.session['currentUrl'] = ''
    request.session['currentIngr'] = ''
    request.session['currentServe'] = ''
    return redirect('/')