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
    

class DisplayPlayerDetailView(generic.DetailView):
    template_name = "players/display_player_detail.html"
    context_object_name = "player"

    def get_queryset(self):
        return Player.objects.all()
    
    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        player = Player.objects.get(slug=self.kwargs['slug'])
        context = {"player": player}


        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.template_name, {**context})

