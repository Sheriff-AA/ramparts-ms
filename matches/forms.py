from django import forms
from personnel.models import Match, Player, MatchEvent
from django.core.exceptions import ValidationError


class MatchCreateForm(forms.ModelForm):
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
        fields = ['opposition_team', 'venue', 'match_date', 'competition', 'away_fixture']
        widgets = {
            'competition': forms.Select(attrs={
                'id': 'competition',
                'placeholder': 'Competition category', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'away_fixture': forms.Select(attrs={
                'id': 'away_fixture',
                'placeholder': 'Is this an away fixture?', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'venue': forms.TextInput(attrs={
                'id': 'venue',
                'placeholder': 'Venue', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'opposition_team': forms.TextInput(attrs={
                'id': 'opposition-team',
                'placeholder': 'Opposition Team', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'match_date': forms.DateTimeInput(attrs={
                'id': 'match-date',
                'placeholder': 'Date',
                'type': 'datetime-local', 
                'class':"py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600",
            }),
        }

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


class MatchEventCreateForm(forms.ModelForm):
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


