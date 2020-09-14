from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import json

from recipes.models import Recipe
from users.models import Favorites, Wishlist, Follow

SUCCESS_RESPONSE = '{"success": true}'
User = get_user_model()


def addFavorite(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = int(body['id'])
        user = request.user
        favoritesCheck = Favorites.objects.filter(
            user_id=user.id, recipe_id=recipe_id).exists()
        if not favoritesCheck:
            Favorites.objects.create(user_id=user.id, recipe_id=recipe_id)
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def removeFavorite(request, recipe_id):
    if request.method == "DELETE":
        user = request.user
        favoritesCheck = Favorites.objects.filter(
            user_id=user.id, recipe_id=recipe_id).exists()
        if favoritesCheck:
            Favorites.objects.filter(
                user_id=user.id, recipe_id=recipe_id).delete()
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def addWishlist(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = int(body['id'])
        user = request.user
        wishlistCheck = Wishlist.objects.filter(
            user_id=user.id, recipe_id=recipe_id).exists()
        if not wishlistCheck:
            Wishlist.objects.create(user_id=user.id, recipe_id=recipe_id)
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def removeWishlist(request, recipe_id):
    if request.method == "DELETE":
        user = request.user
        wishlistCheck = Wishlist.objects.filter(
            user_id=user.id, recipe_id=recipe_id).exists()
        if wishlistCheck:
            Wishlist.objects.filter(
                user_id=user.id, recipe_id=recipe_id).delete()
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def addSubscription(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        following_id = int(body['id'])
        user = request.user
        selfCheck = user.id == following_id
        subCheck = Follow.objects.filter(
            subscriber_id=user.id, following_id=following_id).exists()
        if not subCheck and not selfCheck:
            Follow.objects.create(subscriber_id=user.id,
                                  following_id=following_id)
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def removeSubscription(request, following_id):
    if request.method == "DELETE":
        user = request.user
        subCheck = Follow.objects.filter(
            subscriber_id=user.id, following_id=following_id).exists()
        if subCheck:
            Follow.objects.filter(
                subscriber_id=user.id, following_id=following_id).delete()
            return HttpResponse(SUCCESS_RESPONSE)
    return HttpResponse()


def removeRecipe(request, username, recipe_id):
    if request.user.username == username:
        Recipe.objects.filter(id=recipe_id).delete()
        return redirect(f'/{username}/')
    return redirect(f'/{username}/{recipe_id}/')
