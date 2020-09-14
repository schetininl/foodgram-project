from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feed/", views.feed, name="feed"),

    path("<username>/", views.userPage, name="user"),
    path("<username>/<int:recipe_id>/", views.recipePage, name="recipe"),
]