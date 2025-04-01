from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages


from personnel.models import Player, Match, MatchEvent, Competition, Result 
from matches.forms import MatchCreateForm, MatchEventCreateForm
from personnel.forms import PlayerCreateForm, CompetitionCreateForm, PlayerUpdateForm


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
    

class PlayerDeleteConfirmView(View):
    template_name = "administration/confirm_delete_player.html"
    dashboard_template = "administration/dashboard.html"
    
    def get(self, request, *args, **kwargs):
        """Display confirmation page for deleting a player."""
        player = get_object_or_404(Player, slug=self.kwargs["slug"])
        
        context = {
            "player": player,
        }
        
        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})


class PlayerUpdateView(generic.UpdateView):
    template_name = "players/player_update.html"
    form_class = PlayerUpdateForm
    context_object_name = "player"

    def get_queryset(self):
        player = Player.objects.filter(slug=self.kwargs.get('slug'))
        return player
        
    def get_object(self, queryset=None):
        """
        TBA
        """
        obj = Player.objects.get(slug=self.kwargs.get('slug'))
        return obj
        
    def get_success_url(self):
        obj = Player.objects.get(slug=self.kwargs.get('slug'))
        messages.success(self.request, f"Player '{obj.name}' updated successfully.")
        return reverse("administration:players-list")
    

class PlayerDeleteView(View):
    def post(self, request, *args, **kwargs):
        """Handle the actual deletion after confirmation."""
        player = get_object_or_404(Player, slug=self.kwargs["slug"])
        # player_slug = player.slug
        
        # Store details for success message
        player_details = f"{player.first_name} {player.last_name}"
        
        # Delete the event
        player.delete()
        
        messages.success(request, f"Player '{player_details}' deleted successfully.")
        
        # Redirect back to the match page
        return redirect('administration:players-list')
    

class PlayerDetailView(generic.DetailView):
    template_name = "players/player_detail.html"
    context_object_name = "player"

    def get_queryset(self):
        return Player.objects.all()
    
    def get(self, request, *args, **kwargs):
        """Return the correct response depending on whether the request is from HTMX."""
        player = Player.objects.get(slug=self.kwargs['slug'])
        context = {"player": player}

        dashboard_template = "administration/dashboard.html" 

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, dashboard_template, {"content": self.template_name, **context})
    

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
        match_event = match.events.all()
        context = {
            "form": MatchEventCreateForm(match=match),
            "match": match,
            "match_events": match_event
            }

        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})

    def post(self, request, *args, **kwargs):
        """Handle form submission while keeping the dashboard layout intact."""
        match = get_object_or_404(Match, slug=self.kwargs["slug"])
        match_event = match.events.all()

        form = MatchEventCreateForm(request.POST, match=match)
        context = {
            "form": form, 
            "match": match,
            "match_events": match_event
        }

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


class MatchEventDeleteConfirmView(View):
    template_name = "administration/confirm_delete_match_event.html"
    dashboard_template = "administration/dashboard.html"
    
    def get(self, request, *args, **kwargs):
        """Display confirmation page for deleting a match event."""
        event = get_object_or_404(MatchEvent, id=self.kwargs["event_id"])
        match = event.match
        
        context = {
            "event": event,
            "match": match
        }
        
        if request.htmx:
            return render(request, self.template_name, context)
        
        return render(request, self.dashboard_template, {"content": self.template_name, **context})


class MatchEventDeleteView(View):
    def post(self, request, *args, **kwargs):
        """Handle the actual deletion after confirmation."""
        event = get_object_or_404(MatchEvent, id=self.kwargs["event_id"])
        match = event.match
        match_slug = match.slug
        
        # Store details for success message
        event_details = f"{event.player} - {event.event_type} (Minute: {event.minute})"
        
        # Delete the event
        event.delete()
        
        messages.success(request, f"MatchEvent '{event_details}' deleted successfully.")
        
        # Redirect back to the match page
        return redirect('administration:create-event', slug=match_slug)
    
