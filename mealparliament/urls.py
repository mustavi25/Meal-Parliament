"""
URL configuration for mealparliament project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from households.api_views import HouseholdViewSet, HouseholdMemberViewSet
from meals.api_views import MealItemViewSet, IngredientViewSet, MealSlotViewSet
from accounts.api_views import RegisterView

router = DefaultRouter()
router.register('households', HouseholdViewSet, basename='household')
router.register('household-members', HouseholdMemberViewSet, basename='householdmember')
router.register('meal-items', MealItemViewSet, basename='mealitem')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('meal-slots', MealSlotViewSet, basename='mealslot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('households/', include('households.urls')),
    path('meals/', include('meals.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('api/register/', RegisterView.as_view(), name='register'),

    # API routes
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', obtain_auth_token, name='api_login'),
]