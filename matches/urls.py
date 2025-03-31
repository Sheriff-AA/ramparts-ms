from django.urls import path
from django.views.generic import TemplateView


from .views import DisplayGamesListView

"""
BASE ENDPOINT /
"""
app_name = "matches"


urlpatterns = [
    # path('', LandingPageView.as_view(), name='index'),
    path('', DisplayGamesListView.as_view(), name='matches-list'),
]