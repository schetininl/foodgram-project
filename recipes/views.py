from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
import json

from .models import Recipe
from users.models import Favorites, Wishlist, Follow
from .helper import tagCollect

SUCCESS_RESPONSE = '{"success": true}'
User = get_user_model()


def index(request):
    tags, tagsFilter = tagCollect(request)
    if tagsFilter:
        recipes = Recipe.objects.filter(tagsFilter).order_by("-pk")
    else:
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


def userPage(request, username):
    user = get_object_or_404(User, username=username)
    tags, tagsFilter = tagCollect(request)
    if tagsFilter:
        recipes = Recipe.objects.filter(tagsFilter).filter(
            author_id=user.id).order_by("-pk")
    else:
        recipes = Recipe.objects.filter(author_id=user.id).order_by("-pk")
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
        'wishlistCount': wishlistCount,
        'user': user
    }
    return render(request, 'user_page.html', context)


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


def addSubscription(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = body['id']
        user = request.user
        subCheck = Follow.objects.filter(
            subscriber_id=user.id, following_id=recipe_id).exists()
        if not subCheck:
            Follow.objects.create(subscriber_id=user.id,
                                  following_id=recipe_id)
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
