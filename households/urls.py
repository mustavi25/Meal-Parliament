from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_household_view, name='create_household'),
    path('join/', views.join_household_view, name='join_household'),
]