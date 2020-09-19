from django import template

from users.models import Wishlist

register = template.Library()


@register.filter
def wishlist_count(user):
    return Wishlist.objects.filter(user_id=user.id).count()
