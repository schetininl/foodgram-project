from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<username>/", views.index, name="user"),
    path("<username>/<int:recipe_id>/", views.index, name="recipe")
]