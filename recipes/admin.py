from django.contrib import admin

from .models import Recipe, Dimension, Ingredient, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title")
    search_fields = ("text",)
    list_filter = ("author", "title", "tags")
    inlines = [
        RecipeIngredientInline,
    ]


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("title",)
