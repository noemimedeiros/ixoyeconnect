from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from core.forms import EnderecoForm
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import Contribuicao
from .forms import ContribuicaoForm

class ContribuicaoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_list_view.html'
    model = Contribuicao
    context_object_name = 'contribuicao'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instituicao_id=self.kwargs['instituicao_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Contribuições"
        context["active"] = ["contribuicao"]
        return context

class ContribuicaoCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_create_view.html'
    model = Contribuicao
    form_class = ContribuicaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Contribuição"
        context["active"] = ["contribuicao"]
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
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})
    
class ContribuicaoUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'contribuicao/contribuicao_create_view.html'
    model = Contribuicao
    form_class = ContribuicaoForm
    context_object_name = "contribuicao"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Contribuição"
        context["active"] = ["contribuicao"]
        context["endereco_form"] = EnderecoForm()

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})

@login_required(login_url="/login/")
def ContribuicaoDeleteView(request, pk):
    try:
        Contribuicao.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except Contribuicao.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('contribuicao:contribuicao_list_view', kwargs={'instituicao_pk': request.user.conta.pk}))