from django.shortcuts import render
from django.views import generic
from django.db.models import Q


from personnel.models import Match, MatchEvent, Competition, Result


class DisplayGamesListView(generic.ListView):
    model = Match
    template_name = 'matches/display_matches.html'
    context_object_name = 'matches'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(opposition_name__icontains=query)
            )
        return queryset
    
