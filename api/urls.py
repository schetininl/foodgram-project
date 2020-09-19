from django.urls import path

from . import views


urlpatterns = [
    path("add_favorite",
         views.add_favorite, name="add_favorite"),
    path("remove_favorite/<int:recipe_id>",
         views.remove_favorite, name="remove_favorite"),
    path("add_wishlist",
         views.add_wishlist, name="add_wishlist"),
    path("remove_wishlist/<int:recipe_id>",
         views.remove_wishlist, name="remove_wishlist"),
    path("add_subscription",
         views.add_subscription, name="add_subscription"),
    path("remove_subscription/<int:following_id>",
         views.remove_subscription, name="remove_subscription"),
    path("<username>/<recipe_id>/remove/",
         views.remove_recipe, name="remove_recipe"),
    path("ingredients/",
         views.get_ingredients, name="get_ingredients"),
    path("print_wishlist/",
         views.get_wishlist, name="get_wishlist"),
]
