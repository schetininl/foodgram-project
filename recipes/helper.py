from .models import TAG_CHOICES
from django.db.models import Q
from functools import reduce
import operator


def tag_collect(request):
    """Собирает теги для фильтрации рецептов на странице.
    Логика формирования запроса вынуждает использовать
    Q и reduce"""
    tags = []
    for label, _ in TAG_CHOICES:
        if request.GET.get(label, ""):
            tags.append(label)
    if tags:
        tags_filter = reduce(operator.or_, (Q(tags__contains=tag)
                                           for tag in tags))
        return tags, tags_filter
    else:
        return tags, None
