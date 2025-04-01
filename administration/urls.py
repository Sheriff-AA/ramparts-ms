from django.urls import path
from django.views.generic import TemplateView


from .views import CompetitionCreateView, DashboardHomeView, MatchCreateView, PlayerCreateView, PlayerListView, MatchListView, MatchDetailView, MatchEventCreateView, MatchEventDeleteConfirmView, MatchEventDeleteView, PlayerDeleteConfirmView, PlayerDeleteView, PlayerUpdateView, PlayerDetailView

"""
BASE ENDPOINT /
"""
app_name = "administration"


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('create-competition/', CompetitionCreateView.as_view(), name='create-competition'),
    path('create-match/', MatchCreateView.as_view(), name='create-match'),
    path('create-player/', PlayerCreateView.as_view(), name='create-player'),
    path('create-event/<slug:slug>', MatchEventCreateView.as_view(), name='create-event'),
    # path('success/', TemplateView.as_view(template_name='administration/success.html'), name='success'),
    path('players-list/', PlayerListView.as_view(), name='players-list'),
    path('player-details/<slug:slug>', PlayerDetailView.as_view(), name='player-details'),
    path('match-list/', MatchListView.as_view(), name='match-list'),
    path('match/<slug:slug>', MatchDetailView.as_view(), name='match-details'),
    path('event/<int:event_id>/delete/confirm/', MatchEventDeleteConfirmView.as_view(), name='match-event-delete-confirm'),
    path('event/<int:event_id>/delete/', MatchEventDeleteView.as_view(), name='match-event-delete'),
    path('player/<slug:slug>/delete/confirm/', PlayerDeleteConfirmView.as_view(), name='player-delete-confirm'),
    path('player/<slug:slug>/delete/', PlayerDeleteView.as_view(), name='player-delete'),
    path("player/<slug:slug>/update", PlayerUpdateView.as_view(), name='player-update'),

]