from django import forms
from .models import Household

class CreateHouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['name']


class JoinHouseholdForm(forms.Form):
    invite_code = forms.CharField(max_length=20, label="Invite Code")