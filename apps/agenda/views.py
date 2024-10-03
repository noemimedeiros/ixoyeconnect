from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.views.generic import (DeleteView, DetailView, ListView, UpdateView)

from .models import AgendaSemanal

class AgendaSemanal(LoginRequiredMixin, ListView):
    template_name = 'agenda/agenda_list_view.html'
    model = AgendaSemanal