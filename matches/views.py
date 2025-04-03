from django.shortcuts import render
from django.core.paginator import Paginator
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
                Q(opposition_team__icontains=query)
            )
        return queryset
    
    def manual_pagination(self, request, queryset):
        queryset_paginator = Paginator(queryset, 25)
        queryset_page_number = request.GET.get("page")
        return queryset_paginator.get_page(queryset_page_number)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        search = request.GET.get('search', None)
        date = request.GET.get('match_date', None)
        list_type = self.request.GET.get("list_type", "results")

        if list_type == "fixtures":
            queryset = fixtures = Match.objects.filter(is_fixture=True).order_by('match_date')
        else:
            queryset = Result.objects.all().order_by('-match__match_date')
        

        if search:
            if list_type == "fixtures":
                queryset = queryset.filter(Q(opposition_team__icontains=search))
            else:
                queryset = queryset.filter(Q(match__opposition_team__contains=search))
        if date:
            if list_type == "fixtures":
                queryset = queryset.filter(Q(match_date__date=date))
            else:
                queryset = queryset.filter(Q(match__match_date__date=date))
 
        queryset = self.manual_pagination(request, queryset)

        context.update({
            "queryset": queryset,
            "list_type": list_type,
            "search": self.request.GET.get("search", None),
        })

        if request.htmx:
            if list_type == "fixtures":
                template_name = 'matches/partials/display_match_fixtures.html'
            else:
                template_name = 'matches/partials/display_match_results.html'
            # if search or date:  
            #     template_name = 'matches/partials/partial_match_list.html'
                
            return render(request, template_name, context)
        else:
            template_name = 'matches/display_matches.html'
            return render(request, template_name, context)
    

class DisplayMatchDetailView(generic.DetailView):
    model = Match
    template_name = "matches/display_details.html"
    context_object_name = "match"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.get_object()
        match_events = MatchEvent.objects.filter(match=match).order_by('minute')
        context['match_events'] = match_events
        return context

