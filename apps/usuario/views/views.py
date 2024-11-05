
from django.db.models.base import Model as Model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.shortcuts import get_object_or_404

from allauth.account.views import PasswordChangeView
from django.urls import reverse

from core.forms import MyChangePasswordForm
from usuario.models import InstituicaoSede, Membro
from core.views import MyDetailViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyViewIxoyeConnect

from ..forms import FuncaoForm, NewMembroForm
from core.messages_utils import message_error_generic, message_create_registro
from ..forms import DenominacaoForm, DepartamentoForm, InstituicaoForm

def cadastrar_instituicao(request):
    if request.POST:
        form = InstituicaoForm(request.POST, prefix="instituicao")
        if form.is_valid():
            form.save()
            message_create_registro(request)
        else:
            print(form.errors)
            message_error_generic(request, 'Houve um erro durante o cadastro. Por favor, tente novamente.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cadastrar_denominacao(request):
    if request.POST:
        form = DenominacaoForm(request.POST, prefix="denominacao")
        if form.is_valid():
            form.save()
            message_create_registro(request)
        else:
            print(form.errors)
            message_error_generic(request, 'Houve um erro durante o cadastro. Por favor, tente novamente.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cadastrar_funcao(request):
    if request.POST:
        form = FuncaoForm(request.POST, prefix="funcao")
        if form.is_valid():
            form.save()
            message_create_registro(request)
        else:
            print(form.errors)
            message_error_generic(request, 'Houve um erro durante o cadastro. Por favor, tente novamente.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login/")
def cadastrar_departamento(request):
    if request.POST:
        form = DepartamentoForm(request.POST, prefix="departamento")
        if form.is_valid():
            form.save()
            message_create_registro(request)
        else:
            print(form.errors)
            message_error_generic(request, 'Houve um erro durante o cadastro. Por favor, tente novamente.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ProfileView(LoginRequiredMixin):
    def get_object(self):
        if self.request.user.is_instituicao:
            return get_object_or_404(InstituicaoSede, pk=self.request.user.pk)
        else:
            return get_object_or_404(Membro, pk=self.request.user.pk)
    
class MeuPerfilView(ProfileView, MyUpdateViewIxoyeConnect):
    template_name = 'usuario/perfil/meu_perfil.html'
    form_class = NewMembroForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_instituicao:
            return HttpResponseRedirect(reverse('usuario:instituicao_detail_view', kwargs={'pk': self.request.user.pk}))
        else:
            return HttpResponseRedirect(reverse('usuario:membro_detail_view', kwargs={'pk': self.request.user.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Meu Perfil"
        return context

class SenhaSegurancaView(MyViewIxoyeConnect, ProfileView, PasswordChangeView):
    template_name = 'usuario/perfil/senha_seguranca.html'
    form_class = MyChangePasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Senha e Segurança"
        return context
    
    def get_success_url(self):
        return reverse('usuario:senha_seguranca')
    
class DeletarContaView(ProfileView, MyDetailViewIxoyeConnect):
    template_name = 'usuario/perfil/deletar_conta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Deletar Conta"
        return context