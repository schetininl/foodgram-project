from django.forms import ModelForm
from .models import Recipe


class RecipeForm(ModelForm):
    """Форма создания/редактирования рецепта"""
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'time', 'description', 'image']
