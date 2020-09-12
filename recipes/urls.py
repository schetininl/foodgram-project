from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
   
    path("<username>/", views.index, name="user"),
    path("<username>/<int:recipe_id>/", views.index, name="recipe"),


    path("add_favorite", views.addFavorite, name="add_favorite"),
    path("remove_favorite/<int:recipe_id>", views.removeFavorite, name="remove_favorite"),
    path("add_wishlist", views.addWishlist, name="add_wishlist"),
    path("remove_wishlist/<int:recipe_id>", views.removeWishlist, name="remove_wishlist")
]