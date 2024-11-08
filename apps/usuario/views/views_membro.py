from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse
from django.db.models import Q

from usuario.filter import MembroFilter
from core.forms import EnderecoForm, MySignUpForm
from core.messages_utils import message_delete_registro, message_error_registro, message_success_generic
from core.views import MyCreateViewIxoyeConnect, MyDetailViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from ..models import Departamento, FuncaoDepartamento, Membro, User
from ..forms import FuncaoForm, NewMembroForm, FuncaoMembroFormset, UserForm

from ..forms import DepartamentoForm

class MembroDetailView(LoginRequiredMixin, MyDetailViewIxoyeConnect):
    template_name = 'usuario/membro/membro_profile_view.html'
    model = Membro
    context_object_name = 'membro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Minha Conta"
        context["active"] = ["lista-membros"]
        context["usuario"] = self.request.user.conta
        return context

class MembroListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'usuario/membro/membro_list_view.html'
    model = Membro
    ordering = ['nome']
    context_object_name = 'membro'
    search_fields = ['nome']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(sede_id=self.kwargs['instituicao_pk'], user__is_active=True)
        if self.request.GET:
            qs = MembroFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Membros"
        context["active"] = ["lista-membros"]
        context["filter"] = MembroFilter()
        if self.request.GET:
            context["filter"] = MembroFilter(self.request.GET)
        return context

class MembroCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    template_name = 'usuario/membro/membro_create_view.html'
    model = Membro
    form_class = NewMembroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Criar Membro"
        context["active"] = ["lista-membros"]
        context["endereco_form"] = EnderecoForm()
        context["user_form"] = MySignUpForm()

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST)
            context["user_form"] = MySignUpForm(self.request.POST)

        return context
    
    @transaction.atomic
    def post(self, request):
        form = NewMembroForm(request.POST, request.FILES)
        endereco_form = EnderecoForm(request.POST)
        user_form = MySignUpForm(request.POST)

        if form.is_valid() and endereco_form.is_valid() and user_form.is_valid():
            user = user_form.save(request=request)
            endereco_form = endereco_form.save()
            
            form = form.save(commit=False)
            form.user = user
            form.endereco = endereco_form
            form.sede = self.request.user.instituicao
            form = form.save()
        else:
            self.object = None
            print(form.errors)
            return self.form_invalid(form)
        
        message_success_generic(request, 'Cadastro realizado com sucesso! Por favor, ative sua conta através do link enviado para o seu e-mail.')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sede': self.request.user.instituicao})
        return kwargs
    
    def get_success_url(self):
        return reverse('usuario:membro_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})
    
class MembroUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'usuario/membro/membro_update_view.html'
    model = Membro
    form_class = NewMembroForm
    context_object_name = "membro"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Membro"
        context["active"] = ["lista-membros"]
        membro = self.get_object()

        context["endereco_form"] = EnderecoForm(instance=membro.endereco)
        context["funcoes_form"] = FuncaoMembroFormset(queryset=membro.funcoes.all(), form_kwargs={'membro':membro})
        
        context["departamentos_form"] = DepartamentoForm(instituicao=membro.sede, prefix="departamento")
        context["funcao_form"] = FuncaoForm(instituicao=membro.sede, prefix="funcao")

        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST, instance=membro.endereco)
            context["funcoes_form"] = FuncaoMembroFormset(queryset=membro.funcoes.all(), data=self.request.POST, form_kwargs={'membro':membro})

        return context
    
    def form_valid(self, form):
        membro = self.get_object()
        endereco_form = EnderecoForm(self.request.POST, instance=membro.endereco)
        funcoes_form = FuncaoMembroFormset(queryset=membro.funcoes.all(), data=self.request.POST, form_kwargs={'membro':membro})

        if form.is_valid() and endereco_form.is_valid() and funcoes_form.is_valid():
            form = form.save()
            endereco_form = endereco_form.save()
            funcoes_form.save()
        else:
            self.object = membro
            for funcao in funcoes_form:
                print(funcao.errors)
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sede': self.request.user.instituicao, 'user': self.request.user})
        return kwargs
    
    def get_success_url(self):
        return reverse('usuario:membro_list_view', kwargs={'instituicao_pk': self.request.user.instituicao.pk})


class MembroProfileUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'usuario/membro/membro_profile_update_view.html'
    model = Membro
    form_class = NewMembroForm
    context_object_name = "membro"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Perfil"
        context["active"] = ["membros"]
        membro = self.get_object()
        context["endereco_form"] = EnderecoForm(instance=membro.endereco)
        context["user_form"] = UserForm(instance=membro.user)
        if self.request.POST:
            context["endereco_form"] = EnderecoForm(self.request.POST, instance=membro.endereco)
            context["user_form"] = UserForm(data=self.request.POST, instance=membro.user)
        return context
    
    def form_valid(self, form):
        membro = self.get_object()
        user_form = UserForm(data=self.request.POST, instance=membro.user)
        endereco_form = EnderecoForm(self.request.POST, instance=membro.endereco)
        if form.is_valid() and endereco_form.is_valid() and user_form.is_valid():
            user_form.save()
            form = form.save()
            endereco_form = endereco_form.save()
        else:
            self.object = membro
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sede': self.request.user.instituicao, 'user': self.request.user})
        return kwargs
    
    def get_success_url(self):
        return reverse('usuario:membro_detail_view', kwargs={'pk': self.request.user.pk})

@login_required(login_url="/login/")
def MembroDeleteView(request, pk):
    try:
        User.objects.filter(pk=pk).update(is_active=False)
        message_delete_registro(request)
    except User.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('usuario:membro_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def funcao_por_departamento(request):
    departamentos = Departamento.objects.filter(Q(instituicao__isnull=True) | Q(instituicao=request.user.instituicao))
    departamentos = departamentos.filter(pk=request.GET.get('departamento')).values_list('pk', flat=True)
    funcoes = FuncaoDepartamento.objects.filter(departamento_id__in=departamentos)

    resposta = {
        'id': [],
        'funcao': []
    }
    for funcao in funcoes:
        resposta['id'].append(funcao.funcao.id)
        resposta['funcao'].append(funcao.funcao.funcao)

    return JsonResponse(resposta, safe=False)

@login_required(login_url="/login/")
def devincular_usuario(request, membro_pk):
    try:
        Membro.objects.filter(pk=membro_pk).update(devinculado=1)
        message_delete_registro(request)
    except Membro.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('usuario:membro_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))
