from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from functools import reduce
import operator
import json

from .models import TAG_CHOICES, Recipe
from users.models import Favorites, Wishlist

SUCCESS_RESPONSE = '{"success": true}'


def index(request):
    tags = []
    for label, _ in TAG_CHOICES:
        if request.GET.get(label, ""):
            tags.append(label)
    if tags:
        tagsFilter = reduce(operator.or_, (Q(tags__contains=tag)
                                           for tag in tags))
        recipes = Recipe.objects.filter(tagsFilter).order_by("-pk")
    else:
        tags = [label for label, _ in TAG_CHOICES]
        recipes = Recipe.objects.order_by("-pk")
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    favorites = Favorites.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True)
    wishlist = Wishlist.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True)
    wishlistCount = wishlist.count()
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'favorites': favorites,
        'wishlist': wishlist,
        'wishlistCount': wishlistCount
    }
    return render(request, 'index.html', context)


def addFavorite(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = body['id']
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
        recipe_id = body['id']
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
