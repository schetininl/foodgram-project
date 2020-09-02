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
        User, on_delete=models.CASCADE, related_name="author_recipes", verbose_name="Автор")
    title = models.CharField(max_length=100, verbose_name="Название рецепта")
    tags = MultiSelectField(choices=TAG_CHOICES, blank=True, null=True, verbose_name="Теги")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    time = models.IntegerField(verbose_name="Время приготовления")
    image = models.ImageField(upload_to="recipes/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Рецепты'
        verbose_name_plural = u'Рецепты'


class Dimension(models.Model):
    """Единицы измерения для рецептов"""
    title = models.CharField(max_length=10, verbose_name="Единица измерения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Единицы измерения'
        verbose_name_plural = u'Единицы измерения'


class Ingredient(models.Model):
    """Ингредиенты"""
    title = models.CharField(max_length=25, verbose_name="Ингредиент")
    dimension = models.ForeignKey(
        Dimension, on_delete=models.SET_NULL, null=True, related_name="dimension", verbose_name="Единица измерения")

    def __str__(self):
        return self.title + "/" + self.dimension.title

    class Meta:
        verbose_name = u'Ингредиенты'
        verbose_name_plural = u'Ингредиенты'


class RecipeIngredient(models.Model):
    """Описание ингредиентов и их колличества для рецепта"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe", verbose_name="Рецепт")
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient", verbose_name="Ингредиент")
    amount = models.IntegerField(verbose_name="Количество")
