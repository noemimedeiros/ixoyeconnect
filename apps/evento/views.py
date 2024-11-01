from datetime import date

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from notificacao.models import Notificacao
from evento.filter import EventoFilter
from core.forms import EnderecoForm
from core.messages_utils import message_delete_registro, message_error_registro, message_success_generic
from core.views import MyCreateViewIxoyeConnect, MyDetailViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import Evento, ParticipanteEvento
from .forms import EventoForm

class EventoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'evento/evento_list_view.html'
    model = Evento
    ordering = ['data', 'hora']
    context_object_name = 'eventos'
    search_fields = ['titulo', 'descricao']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(instituicao_id=self.kwargs['instituicao_pk'])
        if self.request.GET:
            qs = EventoFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        hoje = date.today()
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eventos"
        context["active"] = ["evento"]
        context["filter"] = EventoFilter()
        context["eventos_porvir"] = self.get_queryset().filter(data__gte=hoje).order_by('data')
        context["eventos_passados"] = self.get_queryset().filter(data__lt=hoje).order_by('-data')
        if self.request.GET:
            context["filter"] = EventoFilter(self.request.GET)
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
    
    def form_valid(self, form):
        endereco_sede = form.cleaned_data["endereco_sede"]

        form = form.save(commit=False)
        if endereco_sede == False:
            endereco_form = EnderecoForm(self.request.POST)
            if endereco_form.is_valid():
                endereco_form = endereco_form.save()
                form.endereco = endereco_form
        else:
            form.endereco = form.instituicao.endereco

        return super().form_valid(form)
    
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('evento:evento_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})
    
class EventoUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'evento/evento_create_view.html'
    model = Evento
    form_class = EventoForm
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Evento"
        context["active"] = ["evento"]
        context["endereco_form"] = EnderecoForm()

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('evento:evento_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})
    
class EventoDetailView(LoginRequiredMixin, MyDetailViewIxoyeConnect):
    template_name = "evento/evento_detail_view.html"
    model = Evento
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        context["titulo"] = evento.titulo.capitalize()
        context["active"] = ["evento"]
        return context

@login_required(login_url="/login/")
def EventoDeleteView(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
        Notificacao.objects.filter(id_object=pk, modulo=evento.__class__.__name__).delete()
        evento.delete()
        message_delete_registro(request)
    except Evento.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('evento:evento_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def confirmar_participacao_evento(request, evento_pk, membro_pk):
    try:
        ParticipanteEvento.objects.create(evento_id=evento_pk, membro_id=membro_pk)
        message_success_generic(request, "Sua participação está confirmada!")
    except Exception as e:
        print(e)
        message_error_registro(request)
    return HttpResponseRedirect(reverse('evento:evento_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def cancelar_participacao_evento(request, evento_pk, membro_pk):
    try:
        ParticipanteEvento.objects.filter(evento_id=evento_pk, membro_id=membro_pk).delete()
        message_success_generic(request, "Sua participação foi cancelada.")
    except Exception as e:
        print(e)
        message_error_registro(request)
    return HttpResponseRedirect(reverse('evento:evento_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))