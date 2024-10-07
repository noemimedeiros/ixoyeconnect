from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse
from django.views.generic import ListView

from apps.core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateView, MyDeleteView, MyUpdateView

from .models import AgendaSemanal, IconeAgendaSemanal
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
        context["icones"] = IconeAgendaSemanal.objects.all()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})
    
class AgendaSemanalUpdateView(LoginRequiredMixin, MyUpdateView):
    template_name = 'agenda/agenda_create_view.html'
    model = AgendaSemanal
    form_class = AgendaSemanalForm
    context_object_name = "agenda"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Agenda"
        context["icones"] = IconeAgendaSemanal.objects.all()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})

@login_required(login_url="/login/")
def AgendaSemanalDeleteView(request, pk):
    try:
        AgendaSemanal.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except AgendaSemanal.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': request.user.conta.pk}))