from django import forms
from .models import MealSlot, MealItem, Ingredient

class BookMealSlotForm(forms.ModelForm):
    class Meta:
        model = MealSlot
        fields = ['meal_item', 'meal_type', 'meal_date']
        widgets = {
            'meal_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CreateMealItemForm(forms.ModelForm):
    existing_ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Pick from existing ingredients"
    )
    new_ingredients = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Turmeric, Bay Leaf, Yogurt'}),
        label="Add new ingredients (comma-separated)"
    )

    class Meta:
        model = MealItem
        fields = ['title', 'notes', 'meal_type']