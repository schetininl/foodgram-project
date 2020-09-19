from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from users.models import Favorites, Wishlist, Follow
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm
from .helper import tag_collect

User = get_user_model()


def index(request):
    tags, tagsFilter = tag_collect(request)
    if tagsFilter:
        recipes = Recipe.objects.filter(tagsFilter).all()
    else:
        recipes = Recipe.objects.all()
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


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    tags, tagsFilter = tag_collect(request)
    if tagsFilter:
        recipes = Recipe.objects.filter(tagsFilter).filter(
            author_id=user.id).all()
    else:
        recipes = Recipe.objects.filter(author_id=user.id)
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


def recipe_page(request, username, recipe_id):
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
    user = request.user
    following = Follow.objects.filter(
        subscriber=user).values_list("following", flat=True)
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


def new_recipe(request):
    formTitle = 'Создание рецепта'
    btn_caption = "Создать рецепт"
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        ingredients_names = request.POST.getlist('nameIngredient')
        ingredients_values = request.POST.getlist('valueIngredient')
        if len(ingredients_names) == len(ingredients_values):
            count = len(ingredients_names)
        else:
            return redirect("new")
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        for i in range(count):
            RecipeIngredient.add_ingredient(
                RecipeIngredient,
                new_recipe.id,
                ingredients_names[i],
                ingredients_values[i]
            )
        return redirect("index")
    form = RecipeForm()
    wishlistCount = Wishlist.objects.filter(
        user_id=request.user.id).count()
    context = {
        'formTitle': formTitle,
        'btn_caption': btn_caption,
        'form': form,
        'wishlistCount': wishlistCount
    }
    return render(request, 'form_recipe.html', context)


def edit_recipe(request, username, recipe_id):
    formTitle = 'Редактирование рецепта'
    btn_caption = "Сохранить"
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=username)
    recipeRedirect = redirect(
        "recipe", username=user.username, recipe_id=recipe_id)
    is_breakfast = 'breakfast' in recipe.tags
    is_lunch = 'lunch' in recipe.tags
    is_dinner = 'dinner' in recipe.tags
    wishlistCount = Wishlist.objects.filter(
        user_id=request.user.id).count()
    ingredients = RecipeIngredient.objects.filter(
        recipe_id=recipe_id)
    if request.user != user:
        return recipeRedirect
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if request.method == "POST" and form.is_valid():
        ingredients_names = request.POST.getlist('nameIngredient')
        ingredients_values = request.POST.getlist('valueIngredient')
        if len(ingredients_names) == len(ingredients_values):
            count = len(ingredients_names)
        else:
            return redirect("edit_recipe",
                            username=username, recipe_id=recipe_id)
        form.save()
        RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
        for i in range(count):
            RecipeIngredient.add_ingredient(
                RecipeIngredient,
                recipe.id,
                ingredients_names[i],
                ingredients_values[i]
            )
        return recipeRedirect
    context = {
        'formTitle': formTitle,
        'btn_caption': btn_caption,
        'form': form,
        'recipe': recipe,
        'is_breakfast': is_breakfast,
        'is_lunch': is_lunch,
        'is_dinner': is_dinner,
        'ingredients': ingredients,
        'wishlistCount': wishlistCount
    }
    return render(request, 'form_recipe.html', context)


def favorites(request):
    user = request.user
    favorite = Favorites.objects.filter(
        user_id=user.id).values_list("recipe", flat=True)
    tags, tagsFilter = tag_collect(request)
    if tagsFilter:
        recipes = Recipe.objects.filter(tagsFilter).filter(
            id__in=favorite).all()
    else:
        recipes = Recipe.objects.filter(
            id__in=favorite).all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    wishlist = Wishlist.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'wishlist': wishlist,
        'wishlistCount': wishlist.count()
    }
    return render(request, 'favorites.html', context)


def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(
        user_id=user.id).values_list("recipe", flat=True)
    recipes = Recipe.objects.filter(
        id__in=wishlist).all()
    context = {
        'recipes': recipes,
        'wishlistCount': wishlist.count()
    }
    return render(request, 'wishlist.html', context)
