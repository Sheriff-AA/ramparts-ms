from django import forms
from django.core.exceptions import ValidationError
import datetime

from .models import Player, Competition, Result
from utils.current_year import current_year


def year_choices():
    return [(r,r) for r in range(2006, datetime.date.today().year+1)]


class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'name', 'position']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'first_name',
                'placeholder': 'John', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last_name',
                'placeholder': 'Doe', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': "Player's Preferred Name", 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'position': forms.Select(attrs={
                'id': 'position',
                'placeholder': 'Position', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
        }


class CompetitionCreateForm(forms.ModelForm):
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    class Meta:
        model = Competition
        fields = ['category', 'year']
        widgets = {
            'category': forms.Select(attrs={
                'id': 'hs-feedback-post-comment-name-1',
                'placeholder': 'Competition category', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'year': forms.NumberInput(attrs={
                'id': 'hs-feedback-post-comment-email-1',
                'placeholder': 'Year', 
                'class':"py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600",
            }),
        }
        labels = {
            'category': 'Competition Category',
            'year': 'Year',
        }
  

class PlayerUpdateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields =("first_name", "last_name", "name", "position")
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'first_name',
                'placeholder': 'John', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last_name',
                'placeholder': 'Doe', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': "Player's Preferred Name", 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
            'position': forms.Select(attrs={
                'id': 'position',
                'placeholder': 'Position', 
                'class': 'py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600',
            }),
        }

