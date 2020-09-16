from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from multiselectfield import MultiSelectField

User = get_user_model()

# Возможные варианты выбора для поля tags
TAG_CHOICES = (('breakfast', 'Завтрак'),
               ('lunch', 'Обед'),
               ('dinner', 'Ужин'))


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор")
    title = models.CharField(max_length=100, verbose_name="Название рецепта")
    tags = MultiSelectField(choices=TAG_CHOICES, blank=True,
                            null=True, verbose_name="Теги")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание")
    time = models.PositiveIntegerField(verbose_name="Время приготовления")
    image = models.ImageField(
        upload_to="recipes/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Рецепты'
        verbose_name_plural = u'Рецепты'


class Ingredient(models.Model):
    """Ингредиенты"""
    title = models.CharField(
        max_length=25, verbose_name="Название ингредиента")
    dimension = models.CharField(
        max_length=10, verbose_name="Единица измерения")

    def __str__(self):
        return self.title + "/" + self.dimension

    def get_ingredient_name(self):
        return self.title

    class Meta:
        verbose_name = u'Ингредиенты'
        verbose_name_plural = u'Ингредиенты'


class RecipeIngredient(models.Model):
    """Описание ингредиентов и их колличества для рецепта"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    amount = models.PositiveIntegerField(verbose_name="Количество")

    def add_ingredient(self, recipe_id, title, amount):
        ingredient = get_object_or_404(Ingredient, title=title)
        return self.objects.create(recipe_id=recipe_id, ingredient=ingredient, amount=amount)
