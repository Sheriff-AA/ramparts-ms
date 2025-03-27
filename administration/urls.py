from django.urls import path
from django.views.generic import TemplateView


from .views import CompetitionCreateView

"""
BASE ENDPOINT /
"""
app_name = "administration"


urlpatterns = [
    # path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('create-competition/', CompetitionCreateView.as_view(), name='create_competition'),
]