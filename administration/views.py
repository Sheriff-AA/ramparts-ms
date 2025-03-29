from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import View


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


class PlayerCreateView(generic.CreateView):
    model = Player
    form_class = PlayerCreateForm
    template_name = 'administration/create_player.html'
    success_url = '/administration/'

    def form_valid(self, form):
        messages.success(self.request, "Player added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, "Error adding player.")
        return super().form_invalid(form)
    

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
    
