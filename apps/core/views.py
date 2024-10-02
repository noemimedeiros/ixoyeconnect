from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import (View, CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from allauth.account.views import SignupView, LoginView
from django.db import transaction

from instituicao.forms import InstituicaoForm, InstituicaoSedeForm
from core.forms import EnderecoForm, MySignUpForm, MyLoginForm
from usuario.forms import UsuarioForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        return redirect('/login/')
    
class DashboradView(TemplateView):
    template_name = 'core/dashboard.html'

class MyLoginView(LoginView):
    form_class = MyLoginForm

class MyCadastroView(SignupView):
    form_class = MySignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)
            if self.request.POST.get('instituicao'):
                context["instituicaosede_form"] = InstituicaoSedeForm(self.request.POST)
                context["usuario_form"] = UsuarioForm()
            else:
                context["usuario_form"] = UsuarioForm(self.request.POST)
                context["instituicaosede_form"] = InstituicaoSedeForm()
        else:
            context["usuario_form"] = UsuarioForm()
            context["endereco_form"] = EnderecoForm()
            context["instituicaosede_form"] = InstituicaoSedeForm()
        return context

    def get_success_url(self, **kwargs):
        return HttpResponseRedirect(reverse('account_login'))

    @transaction.atomic
    def post(self, request):
        form = MySignUpForm(request.POST)

        if form.is_valid():
            user = form.save(request=request)
        else:
            return self.form_invalid(form)

        endereco_form = EnderecoForm(request.POST)
        if endereco_form.is_valid():
            endereco_form = endereco_form.save()
        else:
            return self.form_invalid(form)
        
        if request.POST.get('instituicao'):
            instituicao_form = InstituicaoSedeForm(request.POST)
            if instituicao_form.is_valid():
                instituicao_form = instituicao_form.save(commit=False)
                instituicao_form.user = user
                instituicao_form.endereco = endereco_form
                instituicao_form = instituicao_form.save()
            else:
                return self.form_invalid(form)
        else:
            usuario_form = UsuarioForm(request.POST)
            if usuario_form.is_valid():
                usuario_form = usuario_form.save(commit=False)
                usuario_form.user = user
                usuario_form.endereco = endereco_form
                usuario_form = usuario_form.save()
            else:
                return self.form_invalid(form)
        return self.get_success_url()
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
    