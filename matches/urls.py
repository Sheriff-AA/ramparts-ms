from django.urls import path
from django.views.generic import TemplateView


from .views import DisplayGamesListView, DisplayMatchDetailView

"""
BASE ENDPOINT /
"""
app_name = "matches"


urlpatterns = [
    # path('', LandingPageView.as_view(), name='index'),
    path('', DisplayGamesListView.as_view(), name='matches-list'),
    path('<slug:slug>/details/', DisplayMatchDetailView.as_view(), name='match-details'),
]