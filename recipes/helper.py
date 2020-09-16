from .models import TAG_CHOICES
from django.db.models import Q
from functools import reduce
import operator


def tagCollect(request):
    """Собирает теги для фильтрации рецептов
    на странице"""
    tags = []
    for label, _ in TAG_CHOICES:
        if request.GET.get(label, ""):
            tags.append(label)
    if tags:
        tagsFilter = reduce(operator.or_, (Q(tags__contains=tag)
                                           for tag in tags))
        return tags, tagsFilter
    else:
        tags = [label for label, _ in TAG_CHOICES]
        return tags, None
