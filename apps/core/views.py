from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.views.generic import (View, CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from allauth.account.views import SignupView, LoginView
from django.db import transaction, IntegrityError
from extra_views import SearchableListMixin

from core.messages_utils import *
from posts.models import CategoriaPost
from usuario.models import Instituicao, InstituicaoSede
from usuario.forms import DenominacaoForm, MembroForm
from usuario.forms import InstituicaoForm, InstituicaoSedeForm
from core.forms import EnderecoForm, MySignUpForm, MyLoginForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        return redirect('/login/')

class MyViewIxoyeConnect:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instituicao"] = self.request.user.instituicao
        context["conteudos"] = CategoriaPost.objects.all()
        return context

class MyTemplateViewIxoyeConnect(MyViewIxoyeConnect, TemplateView):
    pass

class MyDetailViewIxoyeConnect(MyViewIxoyeConnect, DetailView):
    pass
    
class MyListViewIxoyeConnect(MyViewIxoyeConnect, SearchableListMixin, ListView):
    pass
    
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
    
class DashboradView(MyTemplateViewIxoyeConnect):
    template_name = 'core/dashboard.html'

class MyLoginView(LoginView):
    form_class = MyLoginForm

    def get_success_url(self):
        return reverse('core:dashboard')

class MyCadastroView(SignupView):
    form_class = MySignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instituicoes"] = Instituicao.objects.all()
        context["instituicao_form"] = InstituicaoForm(prefix="instituicao")
        context["denominacao_form"] = DenominacaoForm(prefix="denominacao")

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)

            if self.request.POST.get('instituicao'):
                context["instituicaosede_form"] = InstituicaoSedeForm(self.request.POST, prefix="sede")
                context["membro_form"] = MembroForm()
            else:
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

        if request.POST.get('sede-instituicao'):
            membro_instituicao_form = instituicao_form.is_valid()
        else:
            membro_instituicao_form = membro_form.is_valid()

        if form.is_valid() and endereco_form.is_valid() and membro_instituicao_form:
            user = form.save(request=request)
            endereco_form = endereco_form.save()
            
            if request.POST.get('sede-instituicao'):
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
        else:
            return self.form_invalid(form)
        
        message_success_generic(request, 'Cadastro realizado com sucesso! Por favor, ative sua conta através do link enviado para o seu e-mail.')
        return self.get_success_url()
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    