from rest_framework import serializers
from .models import MealItem, Ingredient, MealSlot

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class MealItemSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True, write_only=True, source='ingredients'
    )
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = MealItem
        fields = ['id', 'title', 'notes', 'meal_type', 'created_by', 'created_by_username',
                  'ingredients', 'ingredient_ids', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class MealSlotSerializer(serializers.ModelSerializer):
    meal_item_title = serializers.CharField(source='meal_item.title', read_only=True)
    household_name = serializers.CharField(source='household.name', read_only=True)

    class Meta:
        model = MealSlot
        fields = ['id', 'household', 'household_name', 'meal_item', 'meal_item_title',
                  'meal_type', 'meal_date']