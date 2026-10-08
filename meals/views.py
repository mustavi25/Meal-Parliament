from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from households.models import Household, HouseholdMember
from .models import MealSlot
from .forms import BookMealSlotForm
from .forms import BookMealSlotForm, CreateMealItemForm

def _get_household_if_member(request, household_id):
    """Returns the household only if the logged-in user is actually a member of it."""
    household = get_object_or_404(Household, id=household_id)
    is_member = HouseholdMember.objects.filter(household=household, user=request.user).exists()
    return household if is_member else None


@login_required
def household_meals_view(request, household_id):
    household = _get_household_if_member(request, household_id)
    if not household:
        messages.error(request, "You're not a member of that household.")
        return redirect('dashboard')

    slots = MealSlot.objects.filter(household=household).select_related('meal_item')
    return render(request, 'meals/household_meals.html', {
        'household': household,
        'slots': slots,
    })


@login_required
def book_meal_view(request, household_id):
    household = _get_household_if_member(request, household_id)
    if not household:
        messages.error(request, "You're not a member of that household.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BookMealSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.household = household
            try:
                slot.save()
                messages.success(request, f"Booked {slot.meal_item.title} for {slot.meal_type} on {slot.meal_date}.")
                return redirect('household_meals', household_id=household.id)
            except IntegrityError:
                messages.error(request, f"{household.name} already has a {slot.meal_type} booked for {slot.meal_date}.")
    else:
        form = BookMealSlotForm()

    return render(request, 'meals/book.html', {'form': form, 'household': household})


@login_required
def create_meal_item_view(request):
    if request.method == 'POST':
        form = CreateMealItemForm(request.POST)
        if form.is_valid():
            meal_item = form.save(commit=False)
            meal_item.created_by = request.user
            meal_item.save()

            # attach existing ingredients picked via checkboxes
            meal_item.ingredients.set(form.cleaned_data['existing_ingredients'])

            # create + attach any brand-new ingredients typed in
            new_names = form.cleaned_data['new_ingredients']
            if new_names:
                for name in new_names.split(','):
                    name = name.strip()
                    if name:
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name__iexact=name,
                            defaults={'name': name}
                        )
                        meal_item.ingredients.add(ingredient)

            messages.success(request, f"'{meal_item.title}' created!")
            return redirect('create_meal_item')
    else:
        form = CreateMealItemForm()

    return render(request, 'meals/create_meal_item.html', {'form': form})