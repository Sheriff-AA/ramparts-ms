from django import forms
from .models import Player
from django.core.exceptions import ValidationError


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['opposition_team', 'venue', 'match_date', 'competition']

