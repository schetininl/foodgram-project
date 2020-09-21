from django import template

from recipes.models import TAG_CHOICES

register = template.Library()


@register.filter
def get_tag_value(tag):
    """Возвращает значения тега на русском языке"""
    return dict(TAG_CHOICES)[tag]
