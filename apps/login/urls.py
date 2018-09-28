from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^regi$', views.regi),
    url(r'^loginValidation', views.loginValidation),
    url(r'^regiValidation', views.regiValidation),
    url(r'^$', views.login)
]