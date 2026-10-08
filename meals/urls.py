from django.urls import path
from . import views

urlpatterns = [
    path('<int:household_id>/', views.household_meals_view, name='household_meals'),
    path('<int:household_id>/book/', views.book_meal_view, name='book_meal'),
    path('create/', views.create_meal_item_view, name='create_meal_item'),  
]