from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from usuario.models import FuncaoMembro, InstituicaoSede
from core.messages_utils import message_delete_registro, message_error_registro, message_create_registro, message_update_registro
from core.views import MyCreateViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .filter import EscalaFilter
from .models import Escala
from .forms import EscalaForm

class EscalaListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'escala/escala_list_view.html'
    model = Escala
    ordering = ['data', 'hora']
    context_object_name = 'escalas'
    search_fields = ['titulo', 'descricao']

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.GET:
            return qs.filter(instituicao_id=self.kwargs['instituicao_pk'])
        else:
            return self.filter_queryset(qs)
    
    def filter_queryset(self, queryset):
        funcao_membro = self.request.GET.get('funcao_membro', None)
        if funcao_membro:
            queryset = queryset.filter(funcao_membro_id=funcao_membro)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = InstituicaoSede.objects.get(pk=self.kwargs['instituicao_pk'])
        context["titulo"] = "Escala de Obreiros"
        context["active"] = ["escala"]
        context["form"] = EscalaForm(instituicao=instituicao, prefix="escala")
        context["filter"] = EscalaFilter()

        if self.request.GET:
            if self.request.GET.get("funcao_membro"):
                context["filtrado_para"] = FuncaoMembro.objects.get(pk=self.request.GET.get("funcao_membro"))

            context["filter"] = EscalaFilter(self.request.GET)

        return context

@login_required(login_url="/login/")
def criar_escala(request, instituicao_pk):
    instituicao = InstituicaoSede.objects.get(pk=instituicao_pk)
    form = EscalaForm(request.POST, instituicao=instituicao, prefix="escala")
    if form.is_valid():
        form.save()
        message_create_registro(request)
    else:
        print(form.errors)
        message_error_registro(request)
    return HttpResponseRedirect(reverse('escala:escala_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk})) 

@login_required(login_url="/login/")
def editar_escala(request, pk):
    escala = Escala.objects.get(pk=pk)
    instituicao = escala.instituicao
    form = EscalaForm(request.POST, instance=escala, instituicao=instituicao, prefix="escala")
    if form.is_valid():
        form.save()
        message_update_registro(request)
    else:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('escala:escala_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk})) 

@login_required(login_url="/login/")
def excluir_escala(request, pk):
    try:
        Escala.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except Escala.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('escala:escala_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def funcoes_por_membro(request):
    membro = request.GET.get('membro')
    funcoes = FuncaoMembro.objects.filter(membro_id=membro)
    
    resposta = {
        'id': [],
        'funcao': [],
    }

    for funcao in funcoes:
        resposta['id'].append(funcao.id)
        resposta['funcao'].append(f'{funcao.funcao}')

    return JsonResponse(resposta, safe=False)

@login_required(login_url="/login/")
def carregar_infos_editar(request):
    escala = Escala.objects.filter(pk=request.GET.get('escala_id')).values().first()
    return JsonResponse(escala, safe=False)