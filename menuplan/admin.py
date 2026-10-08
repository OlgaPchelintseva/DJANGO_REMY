from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredients, MealPlan
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure')
    list_filter = ('name', )
    search_fields = ('name', )

class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    list_display = ('name', 'cooking_time', 'cover')
    list_filter = ('name', )
    search_fields = ('name',)

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_date', 'meal_type', 'recipe')
    list_filter = ('meal_date', 'meal_type')
    search_fields = ('meal_date', )