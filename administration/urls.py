from django.urls import path
from django.views.generic import TemplateView


from .views import CompetitionCreateView, DashboardHomeView, MatchCreateView, PlayerCreateView, PlayerListView

"""
BASE ENDPOINT /
"""
app_name = "administration"


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('create-competition/', CompetitionCreateView.as_view(), name='create-competition'),
    path('create-match/', MatchCreateView.as_view(), name='create-match'),
    path('create-player/', PlayerCreateView.as_view(), name='create-player'),
    # path('success/', TemplateView.as_view(template_name='administration/success.html'), name='success'),
    path('players-list/', PlayerListView.as_view(), name='players-list'),
    # path('player-list/<str:slug>', PlayerListView.as_view(), name='player-details'),
    path('match-list/', PlayerListView.as_view(), name='match-list'),
]