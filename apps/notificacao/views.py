from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from notificacao.filter import NotificacaoFilter
from usuario.models import InstituicaoSede, Membro
from notificacao.forms import ConfiguracoesNotificacaoForm
from notificacao.models import ConfiguracoesNotificacao, Notificacao
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

class NotificacaoListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    template_name = 'notificacao/notificacao_list_view.html'
    model = Notificacao
    ordering = ['-data']
    context_object_name = 'notificacoes'
    search_fields = ['mensagem']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user_id=self.request.user.pk)
        if self.request.GET:
            qs = NotificacaoFilter(self.request.GET, queryset=qs).qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Notificações"
        context["active"] = ["notificacao"]
        context["hoje"] = date.today()
        context["ontem"] = date.today() - timedelta(days=1)
        context["nao_lidas"] = self.get_queryset().filter(lida=False)
        context["filter"] = NotificacaoFilter()
        if self.request.GET:
            context["filter"] = NotificacaoFilter(self.request.GET)
        return context
    
class ConfiguracoesNotificacaoView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'usuario/perfil/notificacoes.html'
    model = ConfiguracoesNotificacao
    form_class = ConfiguracoesNotificacaoForm

    def get_object(self):
        if self.request.user.is_admin:
            return get_object_or_404(InstituicaoSede, pk=self.request.user.pk)
        else:
            return get_object_or_404(Membro, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Configurar Notificações"
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    

@login_required(login_url="/login/")
def NotificacaoDeleteView(request, pk):
    try:
        Notificacao.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except Notificacao.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('notificacao:notificacao_list_view', kwargs={'instituicao_pk': request.user.instituicao.pk}))

@login_required(login_url="/login/")
def ler_notificacao(request):
    try:
        Notificacao.objects.filter(pk=request.GET.get('notificacao_id')).update(lida=1)
    except Notificacao.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login/")
def ler_todas_notificacoes(request, user_pk):
    try:
        Notificacao.objects.filter(user_id=user_pk).update(lida=1)
    except Notificacao.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))