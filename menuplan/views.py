from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import RegisterForm, MealPlanForm, ShoppingListPeriodForm
from .models import Ingredient, Recipe, RecipeIngredients, MealPlan


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт создан')
            return redirect('login')
        else:
            messages.error(request, 'Ошибки в форме')
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'page_title': 'Регистрация'
    }
    return render(request, 'menuplan/register.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'menuplan/recipe_list.html', {'recipes': recipes, 'page_title': 'Каталог рецептов'})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredients_list.select_related('product_name').all()
    return render(request, 'menuplan/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients, 'page_title': recipe.name})

@login_required
def add_to_plan(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            try:
                meal_plan = form.save(commit=False)
                meal_plan.user = request.user
                meal_plan.recipe = recipe 
                meal_plan.save()
                messages.success(request, f'Рецепт "{recipe.name}" добавлен в план питания')
                return redirect('recipe_list')
            except Exception as e:
                messages.error(request, 'Такой рецепт уже есть на выбранную дату и прием пищи')
                form = MealPlanForm()
        else:
            messages.error(request, 'Ошибка при добавлении рецепта в план питания')
    else:
        form = MealPlanForm()

    return render(request, 'menuplan/add_to_plan.html', {'form': form, 'recipe': recipe, 'page_title': 'Добавление блюда в план питания'})

@login_required
def my_meal_plan(request):
    meal_plans = MealPlan.objects.filter(user=request.user).order_by('meal_date', 'meal_type')
    return render(request, 'menuplan/my_meal_plan.html', {'meal_plans': meal_plans, 'page_title': 'Мой план питания'})

@login_required
def remove_from_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
    meal_plan.delete()
    messages.success(request, f'Запись удалена')
    return redirect('my_meal_plan')

@login_required
def shopping_list(request):
    items = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        form = ShoppingListPeriodForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            meal_plans = MealPlan.objects.filter(user=request.user, meal_date__range=[start_date, end_date])
            recipe_ids = meal_plans.values_list('recipe_id', flat=True)

            if recipe_ids:
                items = RecipeIngredients.objects.filter(dish_name_id__in=recipe_ids).values('product_name__name', 'product_name__measure').annotate(total_quantity=Sum('quantity_product')).order_by('product_name__name') 
            else:
                items = []
    else:
        form = ShoppingListPeriodForm()
    return render(request, 'menuplan/shopping_list.html', {'form': form, 'items': items, 'start_date': start_date, 'end_date': end_date, 'page_title': 'Список покупок'})