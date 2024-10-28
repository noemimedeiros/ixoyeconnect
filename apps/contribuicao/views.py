from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from contribuicao.filter import ContribuicaoFilter
from usuario.forms import DepartamentoForm
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import Contribuicao
from .forms import ContribuicaoForm

class ContribuicaoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_list_view.html'
    model = Contribuicao
    context_object_name = 'contribuicoes'
    ordering = ['tipo']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(instituicao_id=self.kwargs['instituicao_pk'])
        if self.request.GET:
            qs = ContribuicaoFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Contribuições"
        context["active"] = ["contribuicao"]
        context["filter"] = ContribuicaoFilter()
        if self.request.GET:
            context["filter"] = ContribuicaoFilter(self.request.GET)
        return context

class ContribuicaoCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_create_view.html'
    model = Contribuicao
    form_class = ContribuicaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.request.user.instituicao
        context["titulo"] = "Criar Contribuição"
        context["active"] = ["contribuicao"]
        context["departamentos_form"] = DepartamentoForm(instituicao=instituicao, prefix="departamento")
        return context
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})
    
class ContribuicaoUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_create_view.html'
    model = Contribuicao
    form_class = ContribuicaoForm
    context_object_name = "contribuicao"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.request.user.instituicao
        contribuicao = self.get_object()
        context["titulo"] = "Editar Contribuição"
        context["active"] = ["contribuicao"]
        context["departamentos_form"] = DepartamentoForm(instituicao=instituicao, prefix="departamento")
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})

@login_required(login_url="/login/")
def ContribuicaoDeleteView(request, pk):
    try:
        contribuicao = Contribuicao.objects.get(pk=pk)
        contribuicao.delete()
        message_delete_registro(request)
    except Contribuicao.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))