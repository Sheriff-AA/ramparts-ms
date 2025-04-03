from django.urls import path
from django.views.generic import TemplateView


from .views import DisplayPlayersListView, DisplayPlayerDetailView

"""
BASE ENDPOINT /
"""
app_name = "personnel"


urlpatterns = [
    # path('', LandingPageView.as_view(), name='index'),
    path('players/', DisplayPlayersListView.as_view(), name='players-list'),
    path('players/<slug:slug>', DisplayPlayerDetailView.as_view(), name='player-detail'),
]

