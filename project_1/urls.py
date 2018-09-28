from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.login.urls')),
    url(r'^home', include('apps.sync.urls')),
    url(r'^shop', include('apps.shopList.urls')),
    url(r'^admin/', admin.site.urls)
]
