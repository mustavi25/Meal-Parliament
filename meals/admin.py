from django import forms
from django.contrib import admin
from .models import MealItem, MealSlot, Ingredient

class IngredientAdminForm(forms.ModelForm):
    meal_items = forms.ModelMultipleChoiceField(
        queryset=MealItem.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Meal Items', is_stacked=False),
    )

    class Meta:
        model = Ingredient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['meal_items'].initial = self.instance.meal_items.all()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = ('id', 'name', 'used_in_meals')
    search_fields = ('name',)

    def used_in_meals(self, obj):
        meals = obj.meal_items.all()
        return ", ".join(m.title for m in meals) or "—"
    used_in_meals.short_description = "Used in meal items"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.meal_items.set(form.cleaned_data['meal_items'])


@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'meal_type', 'created_by', 'created_at')
    search_fields = ('title',)
    list_filter = ('meal_type', 'created_at')
    filter_horizontal = ('ingredients',)


@admin.register(MealSlot)
class MealSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'household', 'meal_item', 'meal_type', 'meal_date')
    search_fields = ('household__name', 'meal_item__title')
    list_filter = ('meal_type', 'meal_date', 'household', 'meal_item')