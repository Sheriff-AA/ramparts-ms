"""
URL configuration for rampart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", 
        TemplateView.as_view(template_name="base/landing_page.html"), name="home-page"
        ),
    path("404/", 
        TemplateView.as_view(template_name="base/404_page.html"), name="error-page"
        ),
    path("administration/", include("administration.urls"), name="administration"),
    path("matches/", include("matches.urls"), name="matches"),
    path("personnel/", include("personnel.urls"), name="personnel"),
]

