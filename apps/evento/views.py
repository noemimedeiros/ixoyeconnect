from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from core.forms import EnderecoForm
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import Evento
from .forms import EventoForm

class EventoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'evento/evento_list_view.html'
    model = Evento
    ordering = ['-data', '-hora']
    context_object_name = 'evento'
    search_fields = ['titulo', 'descricao']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instituicao_id=self.kwargs['instituicao_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Evento Semanal"
        context["active"] = ["evento"]
        return context

class EventoCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'evento/evento_create_view.html'
    model = Evento
    form_class = EventoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Evento"
        context["active"] = ["evento"]
        context["endereco_form"] = EnderecoForm()

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('evento:evento_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})
    
class EventoUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'evento/evento_create_view.html'
    model = Evento
    form_class = EventoForm
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Evento"
        context["active"] = ["evento"]
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('evento:evento_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})

@login_required(login_url="/login/")
def EventoDeleteView(request, pk):
    try:
        Evento.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except Evento.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('evento:evento_list_view', kwargs={'instituicao_pk': request.user.conta.pk}))