from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.core.messages_utils import message_error_generic

from .forms import InstituicaoForm

def cadastrar_instituicao(request):
    if request.POST:
        form = InstituicaoForm(request.POST, request.FILES, prefix="instituicao")
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            message_error_generic(request, 'Houve um erro durante o cadastro. Por favor, tente novamente.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))