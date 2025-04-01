from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages


from personnel.models import Player, Match, MatchEvent, Competition, Result 
from matches.forms import MatchCreateForm, MatchEventCreateForm
from personnel.forms import PlayerCreateForm, CompetitionCreateForm


class DashboardHomeView(generic.TemplateView):
    template_name = 'administration/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.all()
        context['matches'] = Match.objects.all()
        context['competitions'] = Competition.objects.all()
        context['results'] = Result.objects.all()
        return context


class CompetitionCreateView(View):
    template_name = "administration/competition_form.html"
    dashboard_template = "administration/dashboard.html" 

    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        context = {"form": CompetitionCreateForm()}

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})  # Full page

    def post(self, request, *args, **kwargs):
        """Handle form submission while keeping the dashboard layout intact."""
        form = CompetitionCreateForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            form.save()
            messages.success(request, "Competition created successfully.")
            context["form"] = CompetitionCreateForm()  # Reset

            if request.htmx:
                return render(request, self.template_name, context)
            
            return render(request, self.dashboard_template, {
                "content": self.template_name,
                **context,
            })
        
        messages.error(self.request, "Error adding competition.")
        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {
            "content": self.template_name,
            **context,
        })


class PlayerCreateView(View):
    template_name = "administration/create_player.html"
    dashboard_template = "administration/dashboard.html" 

    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        context = {"form": PlayerCreateForm()}

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})

    def post(self, request, *args, **kwargs):
        """Handle form submission while keeping the dashboard layout intact."""
        form = PlayerCreateForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            form.save()
            messages.success(request, "Player added successfully.")
            context["form"] = PlayerCreateForm()  # Reset

            if request.htmx:
                return render(request, self.template_name, context)
            
            return render(request, self.dashboard_template, {
                "content": self.template_name,
                **context,
            })
        
        messages.error(self.request, "Error adding player.")
        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {
            "content": self.template_name,
            **context,
        })
    

class MatchCreateView(View):
    template_name = "administration/create_match.html"
    dashboard_template = "administration/dashboard.html" 

    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        context = {"form": MatchCreateForm()}

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})

    def post(self, request, *args, **kwargs):
        """Handle form submission while keeping the dashboard layout intact."""
        form = MatchCreateForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            form.save()
            messages.success(request, "Match created successfully.")
            context["form"] = MatchCreateForm()  # Reset

            if request.htmx:
                return render(request, self.template_name, context)
            
            return render(request, self.dashboard_template, {
                "content": self.template_name,
                **context,
            })
        
        messages.error(self.request, "Error creating match.")
        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {
            "content": self.template_name,
            **context,
        })
    

class PlayerListView(generic.ListView):
    model = Player
    template_name = 'players/player_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(name__icontains=query)
            )
        return queryset
    
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        qs = self.get_queryset()
        if search:
            qs = self.get_queryset().filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))

        paginator = Paginator(qs, 15)
        page_number = request.GET.get("page")
        qs = paginator.get_page(page_number)

        context = {
            'players_qs': qs,
        }

        if request.htmx:
            return render(request, self.template_name, {**context})
        else:
            return render(request, 'administration/dashboard.html', {"content": self.template_name, **context} )
    

class MatchListView(generic.ListView):
    template_name = "matches/match_list.html"
    context_object_name = "matches"

    def get_queryset(self):
        return Match.objects.all().order_by('id')
    
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
            queryset = Match.objects.filter(is_fixture=True).order_by('match_date')
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
            template_name = 'matches/match_list.html'
            if search or date:  
                template_name = 'matches/partials/partial_match_list.html'
                
            return render(request, template_name, context)
        else:
            template_name = 'administration/dashboard.html'
            context['content'] = 'matches/match_list.html'

            return render(request, template_name, context)

    # def get_context_data(self, **kwargs):
    #     context = super(MatchListView, self).get_context_data(**kwargs)

    #     list_type = self.request.GET.get("list_type", "results")

    #     if list_type == "fixtures":
    #         queryset = Match.objects.filter(is_fixture=True).order_by('match_date')
    #     else:
    #         queryset = Result.objects.all().order_by('-match__match_date')

    #     context.update({
    #         "queryset": queryset,
    #         "list_type": list_type,
    #         "search": self.request.GET.get("search", None),
    #     })

    #     return context
    

class MatchDetailView(generic.DetailView):
    model = Match
    template_name = "matches/match_detail.html"
    context_object_name = "match"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.get_object()
        match_events = MatchEvent.objects.filter(match=match).order_by('event_time')
        context['match_events'] = match_events
        context['form'] = MatchEventCreateForm(initial={'match': match})
        return context


class MatchEventCreateView(View):
    template_name = "administration/create_matchevent.html"
    dashboard_template = "administration/dashboard.html"


    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        match = get_object_or_404(Match, slug=self.kwargs["slug"])
        context = {
            "form": MatchEventCreateForm(match=match),
            "match": match
            }

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})

    def post(self, request, *args, **kwargs):
        """Handle form submission while keeping the dashboard layout intact."""
        match = get_object_or_404(Match, slug=self.kwargs["slug"])
        form = MatchEventCreateForm(request.POST, match=match)
        context = {"form": form, "match": match}

        if form.is_valid():
            event = form.save()
            messages.success(request, "Event added successfully.")
            context["form"] = MatchEventCreateForm(match=match)
        

            if request.htmx:
                return render(request, self.template_name, context)
            
            return render(request, self.dashboard_template, {
                "content": self.template_name,
                **context,
            })
        
        messages.error(self.request, "Error adding event.")
        if request.htmx:
            return render(request, self.template_name, {'match': match, **context})
        
        return render(request, self.dashboard_template, {
            "content": self.template_name,
            'match': match,
            **context,
        })
    