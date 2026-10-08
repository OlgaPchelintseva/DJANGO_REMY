from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название продукта')
    measure = models.CharField(max_length=20, choices=[('grams', 'гр.'), ('milliliters', 'мл.'), ('things', 'шт.')], verbose_name='Единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

class Recipe(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название блюда')
    instruction = models.TextField(max_length=1500, verbose_name='Пошаговая инструкция приготовления')
    cooking_time = models.DurationField(null=True, blank=True, verbose_name='Время приготовления')
    cover = models.ImageField(upload_to='cover/', blank=True, null=True, verbose_name='Обложка')

    components = models.ManyToManyField(Ingredient, through='RecipeIngredients', related_name='recipes')

    def __str__(self):
        return f'Рецепт блюда {self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

class RecipeIngredients(models.Model):
    dish_name = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Название блюда', related_name='ingredients_list')
    product_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Название продукта', related_name='used_in')
    quantity_product = models.FloatField(verbose_name='Количество продукта')

    def __str__(self):
        return f'В блюде {self.dish_name.name} - {self.product_name} {self.quantity_product} {self.product_name.get_measure_display()}'

    class Meta:
        verbose_name = 'Состав блюда'
        verbose_name_plural = 'Составы блюд'

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans', verbose_name='Пользователь')
    meal_date = models.DateField(verbose_name='Дата')
    meal_type = models.CharField(max_length=10, default='Breakfast', choices=[('Breakfast', 'Завтрак'), ('Lunch', 'Обед'), ('Dinner', 'Ужин')], verbose_name='Тип приема пищи')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plans', verbose_name='Рецепт')

    def __str__(self):
        return f'План питания для {self.user} на {self.meal_date}'

    class Meta:
        verbose_name = 'План питания'
        verbose_name_plural = 'Список планов питания'
        ordering = ['meal_date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe', 'meal_date', 'meal_type'],
                name='unique_meal_plan_entry'
            )
        ]