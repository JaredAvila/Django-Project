from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/logout', views.logout),
    url(r'^/getRecipe', views.getRecipe),
    url(r'^/foundRecipe', views.foundRecipe),
    url(r'^/nextRecipe', views.nextRecipe),
    url(r'^/prevRecipe', views.prevRecipe),
    url(r'^/addRecipe$', views.addRecipe),
    url(r'^/recipeBox', views.recipeBox),
    url(r'^/viewRecipe/(?P<id>\d+)', views.viewRecipe),
    url(r'^/removeRecipe/(?P<id>\d+)', views.removeRecipe),
    url(r'^/editRecipe/(?P<id>\d+)', views.editRecipe),
    url(r'^/createRecipe', views.createRecipe),
    url(r'^/creation', views.creation),
    url(r'^/viewProfile/(?P<id>\d+)', views.viewProfile),
    url(r'^/editProfile/(?P<id>\d+)', views.editProfile),
    url(r'^/updateUser/(?P<id>\d+)', views.updateUser),
    url(r'^/deletePost/(?P<id>\d+)', views.deletePost),
    url(r'^/addRecipeFromView/(?P<id>\d+)', views.addRecipeFromView),
    url(r'^/wallPost', views.wallPost),
    url(r'^$', views.home)
]