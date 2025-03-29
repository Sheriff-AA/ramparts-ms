from django.urls import path
from django.views.generic import TemplateView


from .views import CompetitionCreateView, DashboardHomeView

"""
BASE ENDPOINT /
"""
app_name = "administration"


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('create-competition/', CompetitionCreateView.as_view(), name='create-competition'),
    path('success/', TemplateView.as_view(template_name='administration/success.html'), name='success'),
    # path('error/', TemplateView.as_view(template_name='administration/error.html'), name='error'),
]