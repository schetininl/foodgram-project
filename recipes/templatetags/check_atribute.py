from django import template

from users.models import Wishlist, Favorites, Follow

register = template.Library()


@register.filter
def check_wishlist(recipe, user):
    """Проверяет добавлен ли рецепт в список покупок"""
    check = Wishlist.objects.filter(
        recipe_id=recipe.id, user_id=user.id).exists()
    return check


@register.filter
def check_favorite(recipe, user):
    """Проверяет добавлен ли рецепт в избранное"""
    check = Favorites.objects.filter(
        recipe_id=recipe.id, user_id=user.id).exists()
    return check


@register.filter
def check_subscription(author, user):
    """Проверяет подписан ли текущий пользователь на автора"""
    check = Follow.objects.filter(
        following=author.id, subscriber=user.id).exists()
    return check
