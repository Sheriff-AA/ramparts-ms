from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


from personnel.models import Player, Match, MatchEvent, Competition, Result


class DisplayPlayersListView(generic.ListView):
    model = Player
    template_name = 'players/squad_display.html'
    context_object_name = 'players'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(name__icontains=query)
            )
        return queryset
    
