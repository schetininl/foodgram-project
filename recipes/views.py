from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Recipe, RecipeIngredient
from users.models import Favorites, Wishlist, Follow
from .helper import tagCollect

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
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'favorites': favorites,
        'wishlist': wishlist,
        'wishlistCount': wishlist.count()
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
    followCheck = Follow.objects.filter(
        following=user.id, subscriber=request.user.id).exists()
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'favorites': favorites,
        'wishlist': wishlist,
        'wishlistCount': wishlist.count(),
        'user': user,
        'followCheck': followCheck
    }
    return render(request, 'user_page.html', context)


def recipePage(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author_id=user.id)
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    favorites = Favorites.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True)
    wishlist = Wishlist.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True)
    followCheck = Follow.objects.filter(
        following=user.id, subscriber=request.user.id).exists()
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'favorites': favorites,
        'wishlist': wishlist,
        'wishlistCount': wishlist.count(),
        'user': user,
        'followCheck': followCheck
    }
    return render(request, 'recipe_page.html', context)


def feed(request):
    user = get_object_or_404(User, id=request.user.id)
    following = Follow.objects.filter(subscriber=user).values_list("following", flat=True)
    authors = User.objects.filter(id__in=following).prefetch_related("recipes")
    paginator = Paginator(authors, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    wishlistCount = Wishlist.objects.filter(
        user_id=request.user.id).count()
    context = {
        'authors': authors,
        'page': page,
        'paginator': paginator,
        'wishlistCount': wishlistCount
    }
    return render(request, 'feed.html', context)
