from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from agenda.filter import AgendaSemanalFilter
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyDeleteViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import AgendaSemanal, IconeAgendaSemanal
from .forms import AgendaSemanalForm

class AgendaSemanalListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'agenda/agenda_list_view.html'
    model = AgendaSemanal
    ordering = ['dia_semana']
    context_object_name = 'agendas'
    search_fields = ['titulo', 'descricao']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(instituicao_id=self.kwargs['instituicao_pk'])
        if self.request.GET:
            qs = AgendaSemanalFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agenda Semanal"
        context["active"] = ["agenda"]
        context["filter"] = AgendaSemanalFilter()
        if self.request.GET:
            context["filter"] = AgendaSemanalFilter(self.request.GET)
        return context

class AgendaSemanalCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'agenda/agenda_create_view.html'
    model = AgendaSemanal
    form_class = AgendaSemanalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Agenda"
        context["active"] = ["agenda"]
        context["icones"] = IconeAgendaSemanal.objects.all()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})
    
class AgendaSemanalUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'agenda/agenda_create_view.html'
    model = AgendaSemanal
    form_class = AgendaSemanalForm
    context_object_name = "agenda"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Agenda"
        context["active"] = ["agenda"]
        context["icones"] = IconeAgendaSemanal.objects.all()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})

@login_required(login_url="/login/")
def AgendaSemanalDeleteView(request, pk):
    try:
        AgendaSemanal.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except AgendaSemanal.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('agenda:agendas_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))