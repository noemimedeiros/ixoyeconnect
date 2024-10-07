from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.views.generic import (View, CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from allauth.account.views import SignupView, LoginView
from django.db import transaction, IntegrityError

from apps.core.messages_utils import *
from usuario.models import Instituicao, InstituicaoSede
from usuario.forms import MembroForm
from usuario.forms import InstituicaoForm, InstituicaoSedeForm
from core.forms import EnderecoForm, MySignUpForm, MyLoginForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        return redirect('/login/')
    
class MyCreateView(CreateView):
    def form_valid(self, form):
        message_create_registro(self.request)
        return super().form_valid(form)

class MyUpdateView(UpdateView):
    def form_valid(self, form):
        message_update_registro(self.request)
        return super().form_valid(form)

class MyDeleteView(DeleteView):
    def form_valid(self, form):
        message_delete_registro(self.request)
        return super().form_valid(form)
    
class DashboradView(TemplateView):
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

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)

            if self.request.POST.get('instituicao'):
                context["instituicaosede_form"] = InstituicaoSedeForm(self.request.POST)
                context["membro_form"] = MembroForm()
            else:
                context["membro_form"] = MembroForm(self.request.POST)
                context["instituicaosede_form"] = InstituicaoSedeForm()
        else:
            context["instituicaosede_form"] = InstituicaoSedeForm()
            context["membro_form"] = MembroForm()
            context["endereco_form"] = EnderecoForm()
        return context

    def get_success_url(self, **kwargs):
        return HttpResponseRedirect(reverse('account_login'))

    @transaction.atomic
    def post(self, request):
        form = MySignUpForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        instituicao_form = InstituicaoSedeForm(request.POST)
        membro_form = MembroForm(request.POST)

        if request.POST.get('instituicao'):
            membro_instituicao_form = instituicao_form.is_valid()
        else:
            membro_instituicao_form = membro_form.is_valid()

        if form.is_valid() and endereco_form.is_valid() and membro_instituicao_form:
            user = form.save(request=request)
            endereco_form = endereco_form.save()
            
            if request.POST.get('instituicao'):
                instituicao_form = instituicao_form.save(commit=False)
                instituicao_form.user = user
                instituicao_form.endereco = endereco_form
                instituicao_form.instituicao_id = request.POST.get('instituicao')
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
    