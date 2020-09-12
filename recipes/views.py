from django.shortcuts import render
from django.core.paginator import Paginator
import operator
from django.db.models import Q
from functools import reduce

from .models import TAG_CHOICES, Recipe


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
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
    )
