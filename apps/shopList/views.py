from django.shortcuts import render, redirect
from apps.login.models import User
from apps.shopList.models import *
from django.contrib import messages

def shopList(request):
    items = Item.objects.all()
    checked = Checked.objects.all()
    return render(request, 'shopList/shop.html', {"items": items, "checked": checked})

def add2List(request):
    if request.POST['name'] == '':
        errors = {}
        errors['error'] = '*Cannot leave blank'
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
        return redirect('/shop')
    user = User.objects.get(hId=request.session['hId'])
    name = request.POST['name']
    item = Item(name = name, userItem = user)
    item.save()
    items = Item.objects.all()
    checked = Checked.objects.all()
    return render(request, 'shopList/listAjax.html', {"items": items, "checked": checked})

def add2ListSync(request):
    if request.POST['name'] == '':
        errors = {}
        errors['error'] = '*Cannot leave blank'
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
        return redirect('/home')
    user = User.objects.get(hId=request.session['hId'])
    name = request.POST['name']
    item = Item(name = name, userItem = user)
    item.save()
    items = Item.objects.all()
    return render(request, 'sync/shopAjax.html', {"items": items})

def checked(request):
    user = User.objects.get(hId=request.session['hId'])
    name = request.POST['name']
    item = Checked(name = name, userItem = user)
    item.save()
    return redirect('/shop')

def unCheck(request, id):
    checked = Checked.objects.get(id = id)
    item = Item(name=checked.name, userItem=checked.userChecked)
    item.save()
    checked.delete()
    items = Item.objects.all()
    checked = Checked.objects.all()
    return render(request, 'shopList/listAjax.html', {"items": items, "checked": checked})

def remove(request, id):
    item = Item.objects.get(id=id)
    checked = Checked(name=item.name, userChecked=item.userItem)
    checked.save()
    item.delete()
    items = Item.objects.all()
    checked = Checked.objects.all()
    return render(request, 'shopList/listAjax.html', {"items": items, "checked": checked})

def removeSync(request, id):
    item = Item.objects.get(id=id)
    checked = Checked(name=item.name, userChecked=item.userItem)
    checked.save()
    item.delete()
    items = Item.objects.all()
    return render(request, 'sync/shopAjax.html', {"items": items})

def delete(request, id):
    item = Checked.objects.get(id=id)
    item.delete()
    items = Item.objects.all()
    checked = Checked.objects.all()
    return render(request, 'shopList/listAjax.html', {"items": items, "checked": checked})