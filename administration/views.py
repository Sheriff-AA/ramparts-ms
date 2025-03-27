from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages


from personnel.models import Player, Match, MatchEvent, Competition, Result 
from matches.forms import MatchForm, MatchEventForm
from personnel.forms import PlayerForm, CompetitionForm


class CompetitionCreateView(generic.CreateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'administration/competition_form.html'
    success_url = '/administration/competitions/'

    def form_valid(self, form):
        messages.success(self.request, "Competition created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating competition.")
        return super().form_invalid(form)