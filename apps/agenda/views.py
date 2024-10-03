from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.views.generic import (DeleteView, DetailView, ListView, UpdateView, CreateView)

from .models import AgendaSemanal
from .forms import AgendaSemanalForm

class AgendaSemanalListView(LoginRequiredMixin, ListView):
    template_name = 'agenda/agenda_list_view.html'
    model = AgendaSemanal

class AgendaSemanalCreateView(LoginRequiredMixin, CreateView):
    template_name = 'agenda/agenda_create_view.html'
    model = AgendaSemanal
    form_class = AgendaSemanalForm