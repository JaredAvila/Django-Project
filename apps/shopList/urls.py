from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/add2List$', views.add2List),
    url(r'^/add2ListSync', views.add2ListSync),
    url(r'^/remove/(?P<id>\d+)', views.remove),
    url(r'^/removeSync/(?P<id>\d+)', views.removeSync),
    url(r'^/checked', views.checked),
    url(r'^/unCheck/(?P<id>\d+)', views.unCheck),
    url(r'^/delete/(?P<id>\d+)', views.delete),
    url(r'^$', views.shopList)
]