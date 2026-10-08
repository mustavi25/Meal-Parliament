from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Household, HouseholdMember
from .forms import CreateHouseholdForm, JoinHouseholdForm


@login_required
def create_household_view(request):
    if request.method == 'POST':
        form = CreateHouseholdForm(request.POST)
        if form.is_valid():
            household = form.save()
            HouseholdMember.objects.create(
                household=household,
                user=request.user,
                role='admin'
            )
            messages.success(request, f"'{household.name}' created! Invite code: {household.invite_code}")
            return redirect('dashboard')
    else:
        form = CreateHouseholdForm()
    return render(request, 'households/create.html', {'form': form})


@login_required
def join_household_view(request):
    if request.method == 'POST':
        form = JoinHouseholdForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['invite_code'].strip().upper()
            try:
                household = Household.objects.get(invite_code=code)
            except Household.DoesNotExist:
                messages.error(request, "No household found with that invite code.")
                return render(request, 'households/join.html', {'form': form})

            already_member = HouseholdMember.objects.filter(household=household, user=request.user).exists()
            if already_member:
                messages.info(request, f"You're already a member of '{household.name}'.")
            else:
                HouseholdMember.objects.create(household=household, user=request.user, role='member')
                messages.success(request, f"Joined '{household.name}'!")
            return redirect('dashboard')
    else:
        form = JoinHouseholdForm()
    return render(request, 'households/join.html', {'form': form})