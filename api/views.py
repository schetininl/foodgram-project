import json
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from recipes.models import Recipe, Ingredient, RecipeIngredient
from users.models import Favorites, Wishlist, Follow

SUCCESS_RESPONSE = JsonResponse({"success": True})
FAIL_RESPONSE = HttpResponse()


@require_http_methods(["POST"])
def add_favorite(request):
    body = json.loads(request.body)
    recipe_id = int(body['id'])
    user = request.user
    _, created = Favorites.objects.get_or_create(
        user_id=user.id, recipe_id=recipe_id)
    return SUCCESS_RESPONSE if created else FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_favorite(request, recipe_id):
    user = request.user
    _, deleted = Favorites.objects.filter(
        user_id=user.id, recipe_id=recipe_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


@require_http_methods(["POST"])
def add_wishlist(request):
    body = json.loads(request.body)
    recipe_id = int(body['id'])
    user = request.user
    _, created = Wishlist.objects.get_or_create(
        user_id=user.id, recipe_id=recipe_id)
    return SUCCESS_RESPONSE if created else FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_wishlist(request, recipe_id):
    user = request.user
    _, deleted = Wishlist.objects.filter(
        user_id=user.id, recipe_id=recipe_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


@require_http_methods(["POST"])
def add_subscription(request):
    body = json.loads(request.body)
    following_id = int(body['id'])
    user = request.user
    if user.id != following_id:
        _, created = Follow.objects.get_or_create(
            subscriber_id=user.id, following_id=following_id)
    return SUCCESS_RESPONSE if created else FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_subscription(request, following_id):
    user = request.user
    _, deleted = Follow.objects.filter(
        subscriber_id=user.id, following_id=following_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


def remove_recipe(request, username, recipe_id):
    if request.user.username == username:
        Recipe.objects.filter(id=recipe_id).delete()
        return redirect("user", username)
    return redirect("recipe", username, recipe_id)


@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get("query").lower()
    ingredients = Ingredient.objects.filter(
        title__contains=query).values("title", "dimension")
    return JsonResponse(list(ingredients), safe=False)


def get_wishlist(request):
    """"Вывод списка покупок в текстовый файл"""
    user = request.user
    wishlist_filter = Wishlist.objects.filter(
        user_id=user.id).values_list("recipe", flat=True)
    ingredient_filter = RecipeIngredient.objects.filter(
        recipe_id__in=wishlist_filter).order_by('ingredient')
    ingredients = {}
    for ingredient in ingredient_filter:
        if ingredient.ingredient in ingredients.keys():
            ingredients[ingredient.ingredient] += ingredient.amount
        else:
            ingredients[ingredient.ingredient] = ingredient.amount

    wishlist = []
    for k, v in ingredients.items():
        wishlist.append(f'{k.title} - {v} {k.dimension} \n')
    wishlist.append('\n\n\n\n')
    wishlist.append('foodgram')

    response = HttpResponse(wishlist, 'Content-Type: text/plain')
    response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
    return response
