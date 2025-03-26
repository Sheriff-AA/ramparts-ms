from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Create your views here.
