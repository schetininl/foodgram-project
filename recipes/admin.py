from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    """Связующая модель для указания ингредиентов в рецептах
    используется в качестве Inline"""
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель Рецепты регистрируется в админ-панели"""
    list_display = ("pk", "author", "title")
    search_fields = ("text",)
    list_filter = ("author", "title", "tags")
    inlines = [
        RecipeIngredientInline,
    ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель Ингредиенты регистрируется в админ-панели"""
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("title",)
