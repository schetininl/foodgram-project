from django.shortcuts import render
from django.http import HttpResponse

from .models import Recipe


def index(request):
    latest = Recipe.objects.order_by("-pk")[:6]
    return render(request, "index.html", {"recipes": latest})
