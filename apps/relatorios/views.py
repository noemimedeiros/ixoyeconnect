from datetime import date, datetime
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.shortcuts import render
from django.urls import reverse

from usuario.models import InstituicaoSede
from relatorios.filter import RelatorioCultoFilter
from relatorios.forms import RelatorioCultoForm
from relatorios.models import AtividadesCulto, RelatorioCulto
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyListViewIxoyeConnect, MyCreateViewIxoyeConnect, MyUpdateViewIxoyeConnect

class RelatorioCultoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'relatorios/relatorio_list_view.html'
    model = RelatorioCulto
    ordering = ['data']
    context_object_name = 'relatorios'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(instituicao_id=self.kwargs['instituicao_pk'])
        if self.request.GET:
            qs = RelatorioCultoFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = InstituicaoSede.objects.get(pk=self.kwargs['instituicao_pk'])
        context["titulo"] = "Relatório de Cultos"
        context["active"] = ["relatorio"]
        context["filter"] = RelatorioCultoFilter()
        if self.request.GET:
            context["filter"] = RelatorioCultoFilter(self.request.GET)
        return context

class RelatorioCultoCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'relatorios/relatorio_create_view.html'
    model = RelatorioCulto
    form_class = RelatorioCultoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Relatório"
        context["active"] = ["relatorio"]
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('relatorio:relatorio_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})

class RelatorioCultoUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'relatorios/relatorio_create_view.html'
    model = RelatorioCulto
    form_class = RelatorioCultoForm
    context_object_name = "relatorio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Relatório"
        context["active"] = ["relatorio"]
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('relatorio:relatorio_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})

@login_required(login_url="/login/")
def RelatorioCultoDeleteView(request, pk):
    try:
        RelatorioCulto.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except RelatorioCulto.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('relatorio:relatorio_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def RelatorioImprimir(request, instituicao_pk):
    qs = RelatorioCulto.objects.filter(instituicao_id=instituicao_pk)
    qs = RelatorioCultoFilter(request.GET, queryset=qs).qs
    hoje = date.today()
    hoje = datetime.strftime(hoje, '%d/%m/%Y')

    context = {
        'instituicao': InstituicaoSede.objects.get(pk=instituicao_pk),
        'filtragem': request.GET,
        'relatorios': qs,
        'hoje': hoje
    }
    return render(request, 'relatorios/relatorio_imprimir.html', context=context)