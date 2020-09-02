from django.db import models
from django.contrib.auth import get_user_model

from multiselectfield import MultiSelectField

User = get_user_model()

# Возможные варианты выбора для поля tags
TAG_CHOICES = (('breakfast', 'Завтрак'),
               ('lunch', 'Обед'),
               ('dinner', 'Ужин'))


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_recipes")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = MultiSelectField(choices=TAG_CHOICES)
    time = models.IntegerField()


class RecipeIngredient(models.Model):
    """Описание ингредиентов и их колличества для рецепта"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe")
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient")
    amount = models.IntegerField()


class Ingredient(models.Model):
    """Ингредиенты"""
    title = models.CharField(max_length=25)
    dimension = models.ForeignKey(Dimension, related_name="dimension")


class Dimension(models.Model):
    """Единицы измерения для рецептов"""
    title = models.CharField(max_length=10)
