from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse
from django.views.generic import ListView

from core.views import MyCreateView

from .models import AgendaSemanal
from .forms import AgendaSemanalForm

class AgendaSemanalListView(LoginRequiredMixin, ListView):
    template_name = 'agenda/agenda_list_view.html'
    model = AgendaSemanal
    ordering = ['dia_semana']
    context_object_name = 'agendas'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instituicao_id=self.kwargs['instituicao_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agenda Semanal"
        return context

class AgendaSemanalCreateView(LoginRequiredMixin, MyCreateView):
    template_name = 'agenda/agenda_create_view.html'
    model = AgendaSemanal
    form_class = AgendaSemanalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Agenda"
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})