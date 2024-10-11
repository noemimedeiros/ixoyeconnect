from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.core.messages_utils import message_error_generic, message_create_registro

from .forms import DenominacaoForm, DepartamentoForm, InstituicaoForm

def cadastrar_instituicao(request):
    if request.POST:
        form = InstituicaoForm(request.POST, request.FILES, prefix="instituicao")
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