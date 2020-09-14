from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("feed/", views.feed, name="feed"),
    path("new/", views.newRecipe, name="new"),
    path("favorites/", views.favorites, name="favorites"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("print_wishlist/", views.printWishlist, name="print_wishlist"),
    path("<username>/", views.userPage, name="user"),
    path("<username>/<int:recipe_id>/", views.recipePage, name="recipe"),
    path("<username>/<recipe_id>/edit/", views.editRecipe, name="edit_recipe")
]
