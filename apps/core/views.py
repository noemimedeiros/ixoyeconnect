from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import (View, CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from allauth.account.views import SignupView
from django.db import transaction

from core.forms import EnderecoForm, SignUpForm
from usuario.forms import UsuarioForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        return redirect('/login/')
    
class DashboradView(TemplateView):
    template_name = 'core/dashboard.html'

class CadastroView(SignupView):
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["usuario_form"] = UsuarioForm(self.request.POST)
            context["endereco_form"] = EnderecoForm(self.request.POST)
        else:
            context["usuario_form"] = UsuarioForm()
            context["endereco_form"] = EnderecoForm()
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        print(self.request.POST)
        usuario_form = UsuarioForm(self.request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
        else:
            return self.form_inoknvalid(form)

        endereco_form = EnderecoForm(self.request.POST)
        if endereco_form.is_valid():
            endereco_form.save()
        else:
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
    