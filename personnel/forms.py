from django import forms
from django.core.exceptions import ValidationError


from .models import Player, Competition, Result


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['opposition_team', 'venue', 'match_date', 'competition']


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['category', 'year']

