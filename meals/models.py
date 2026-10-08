from django.db import models
from django.contrib.auth.models import User
from households.models import Household

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class MealItem(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_items')
    ingredients = models.ManyToManyField(Ingredient, related_name='meal_items', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_meal_type_display()})"


class MealSlot(models.Model):
    MEAL_TYPE_CHOICES = MealItem.MEAL_TYPE_CHOICES

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='meal_slots')
    meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE, related_name='bookings')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    meal_date = models.DateField()

    class Meta:
        unique_together = ('household', 'meal_type', 'meal_date')
        ordering = ['meal_date', 'meal_type']

    def __str__(self):
        return f"{self.household.name} — {self.meal_item.title} ({self.meal_type} on {self.meal_date})"