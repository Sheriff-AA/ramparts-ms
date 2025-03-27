from django import forms
from personnel.models import Match, Player, MatchEvent
from django.core.exceptions import ValidationError


class MatchForm(forms.ModelForm):
    selected_line_up = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    selected_substitutes = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Match
        fields = ['opposition_team', 'venue', 'match_date', 'competition']

    def clean(self):
        """Perform the same validations as in the model"""
        cleaned_data = super().clean()
        line_up = cleaned_data.get('selected_line_up', [])
        substitutes = cleaned_data.get('selected_substitutes', [])

        # Ensure lineup does not exceed 11 players
        if len(line_up) > 11:
            raise ValidationError("A starting lineup can have at most 11 players.")

        # Ensure no player is in both lineup and substitutes
        overlap = set(line_up) & set(substitutes)
        if overlap:
            raise ValidationError(f"Players {', '.join([p.name for p in overlap])} cannot be both in lineup and substitutes.")

        return cleaned_data

    def save(self, commit=True):
        match = super().save(commit=False)

        # Convert selected players to names before saving
        match.line_up = list(self.cleaned_data['selected_line_up'].values_list('name', flat=True))
        match.substitutes = list(self.cleaned_data['selected_substitutes'].values_list('name', flat=True))

        if commit:
            match.save()
        return match


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = MatchEvent
        fields = ["match", "player", "event_type", "minute", "additional_info"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.match:
            allowed_players = self.instance.match.line_up + self.instance.match.substitutes
            self.fields["player"].widget = forms.Select(choices=[(p, p) for p in allowed_players])

    def clean_player(self):
        player = self.cleaned_data.get("player")
        match = self.cleaned_data.get("match")

        if match:
            allowed_players = set(match.line_up + match.substitutes)
            if player not in allowed_players:
                raise ValidationError(f"Player {player} is not in the lineup or substitutes for this match.")

        return player


