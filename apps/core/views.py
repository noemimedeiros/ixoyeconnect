from datetime import date
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template
from django.views.generic import (View, CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from allauth.account.views import SignupView, LoginView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.db import transaction
from extra_views import SearchableListMixin

from escala.models import Escala
from notificacao.models import ConfiguracoesNotificacao, Notificacao
from core.messages_utils import *
from posts.models import CategoriaPost
from usuario.models import InstituicaoSede
from usuario.forms import DenominacaoForm, MembroForm
from usuario.forms import InstituicaoSedeForm
from core.forms import EnderecoForm, MySignUpForm, MyLoginForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        return redirect('/login/')

class MyViewIxoyeConnect:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user.conta, 'desvinculado'):
                if request.user.conta.desvinculado:
                    logout(request)
                    return render(request, 'account/desvinculado.html')
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instituicao"] = self.request.user.instituicao
        context["conteudos"] = CategoriaPost.objects.all()
        context["usuario"] = self.request.user.conta
        return context

class MyTemplateViewIxoyeConnect(MyViewIxoyeConnect, TemplateView):
    pass

class MyDetailViewIxoyeConnect(MyViewIxoyeConnect, DetailView):
    pass
    
class MyListViewIxoyeConnect(MyViewIxoyeConnect, SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            filtros_aplicados = {k: v for k, v in self.request.GET.items() if v and v != ['']}
            context["filtros_aplicados"] = len(filtros_aplicados)
        return context
    
class MyCreateViewIxoyeConnect(MyViewIxoyeConnect, CreateView):
    def form_valid(self, form):
        message_create_registro(self.request)
        return super().form_valid(form)

class MyUpdateViewIxoyeConnect(MyViewIxoyeConnect, UpdateView):
    def form_valid(self, form):
        message_update_registro(self.request)
        return super().form_valid(form)

class MyDeleteViewIxoyeConnect(MyViewIxoyeConnect, DeleteView):
    def form_valid(self, form):
        message_delete_registro(self.request)
        return super().form_valid(form)
    
class DashboradView(LoginRequiredMixin, MyTemplateViewIxoyeConnect):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.request.user.instituicao
        context["escala_hoje"] = Escala.objects.filter(instituicao=instituicao, data=date.today())

        return context
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_instituicao:
                self.template_name = 'core/dashboard_instituicao.html'
                get_template(self.template_name)
            else:
                self.template_name = 'core/dashboard_membro.html'
                get_template(self.template_name)
        return super().dispatch(request, *args, **kwargs)

class MyLoginView(LoginView):
    form_class = MyLoginForm

    def get_success_url(self):
        return reverse('core:dashboard')

class MyCadastroView(SignupView):
    form_class = MySignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["instituicoes"] = Instituicao.objects.all()
        # context["instituicao_form"] = InstituicaoForm(prefix="instituicao")
        context["denominacao_form"] = DenominacaoForm(prefix="denominacao")

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)
            context["tipo_cadastro"] = self.request.POST.get('tipo_cadastro')
            if self.request.POST.get('tipo_cadastro') == "igreja":
                context["instituicaosede_form"] = InstituicaoSedeForm(self.request.POST, prefix="sede")
                context["instituicao_selecionada"] = self.request.POST.get('sede-instituicao')
                context["membro_form"] = MembroForm()
            if self.request.POST.get('tipo_cadastro') == "membro":
                context["membro_form"] = MembroForm(self.request.POST)
                context["instituicaosede_form"] = InstituicaoSedeForm(prefix="sede")
        else:
            context["instituicaosede_form"] = InstituicaoSedeForm(prefix="sede")
            context["membro_form"] = MembroForm()
            context["endereco_form"] = EnderecoForm()
        return context

    def get_success_url(self, **kwargs):
        return HttpResponseRedirect(reverse('account_login'))

    @transaction.atomic
    def post(self, request):
        form = MySignUpForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        instituicao_form = InstituicaoSedeForm(request.POST, request.FILES, prefix="sede")
        membro_form = MembroForm(request.POST, request.FILES)

        if self.request.POST.get('tipo_cadastro') == "igreja":
            membro_instituicao_form = instituicao_form.is_valid()
        if self.request.POST.get('tipo_cadastro') == "membro":
            membro_instituicao_form = membro_form.is_valid()

        if form.is_valid() and endereco_form.is_valid() and membro_instituicao_form:
            user = form.save(request=request)
            endereco_form = endereco_form.save()
            
            if self.request.POST.get('tipo_cadastro') == "igreja":
                instituicao_form = instituicao_form.save(commit=False)
                instituicao_form.user = user
                instituicao_form.endereco = endereco_form
                instituicao_form.instituicao_id = request.POST.get('sede-instituicao')
                instituicao_form = instituicao_form.save()
            else:
                membro_form = membro_form.save(commit=False)
                membro_form.user = user
                membro_form.endereco = endereco_form
                membro_form.sede = InstituicaoSede.objects.get(codigo=request.POST.get('codigo_sede'))
                membro_form = membro_form.save()
            
            ConfiguracoesNotificacao.objects.create(user=user)
        else:
            return self.form_invalid(form)
        
        message_success_generic(request, 'Cadastro realizado com sucesso!')
        return self.get_success_url()
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class MyRecuperarSenhaKeyDone(PasswordResetFromKeyDoneView):
    def dispatch(self, request, *args, **kwargs):
        message_success_generic(request, 'Senha alterada com sucesso.')
        return redirect('/login/')