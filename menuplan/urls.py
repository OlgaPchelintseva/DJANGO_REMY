from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('add-to-plan/<int:recipe_id>', views.add_to_plan, name='add_to_plan'),
    path('my-meal-plan/', views.my_meal_plan, name='my_meal_plan'),
    path('remove-from-plan/<int:meal_plan_id>/', views.remove_from_plan, name='remove_from_plan'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
]