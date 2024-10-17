from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from core.forms import EnderecoForm
from core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyUpdateViewIxoyeConnect, MyDetailViewIxoyeConnect

from ..models import InstituicaoSede
from ..forms import InstituicaoSedeForm, RedeSocialInstituicaoSedeFormset, UserForm

class InstituicaoSedeDetailView(LoginRequiredMixin, MyDetailViewIxoyeConnect):
    template_name = 'usuario/instituicao/instituicao_profile_view.html'
    model = InstituicaoSede
    context_object_name = 'igreja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.get_object()
        if self.request.user.is_instituicao:
            context["titulo"] = "Minha Conta"
        else:
            context["titulo"] = "Igreja"
        context["active"] = ["instituicao"]
        context["usuario"] = self.request.user.conta
        return context
    
class InstituicaoSedeUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    template_name = 'usuario/instituicao/instituicao_profile_update_view.html'
    model = InstituicaoSede
    form_class = InstituicaoSedeForm
    context_object_name = "instituicao"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Instituição"
        context["active"] = ["instituicao"]
        instituicao = self.get_object()
        context["user_form"] = UserForm(instance=instituicao.user)
        context["endereco_form"] = EnderecoForm(instance=instituicao.endereco)
        context["redessociais_form"] = RedeSocialInstituicaoSedeFormset(queryset=instituicao.redes_sociais.all(), form_kwargs={'instituicao':instituicao})
        if self.request.POST:
            context["user_form"] = UserForm(self.request.POST, instance=instituicao.user)
            context["endereco_form"] = EnderecoForm(self.request.POST, instance=instituicao.endereco)
            context["redessociais_form"] = RedeSocialInstituicaoSedeFormset(queryset=instituicao.redes_sociais.all(), data=self.request.POST, form_kwargs={'instituicao':instituicao})
        return context
    
    def form_valid(self, form):
        instituicao = self.get_object()
        user_form = UserForm(instance=instituicao.user)
        endereco_form = EnderecoForm(self.request.POST, instance=instituicao.endereco)
        redessociais_form = RedeSocialInstituicaoSedeFormset(data=self.request.POST, form_kwargs={'instituicao':instituicao})

        if form.is_valid() and endereco_form.is_valid() and redessociais_form.is_valid():
            user_form.save()
            form = form.save()
            endereco_form = endereco_form.save()
            redessociais_form.save()
        else:
            print(redessociais_form.errors)
            self.object = instituicao
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('usuario:instituicao_detail_view', kwargs={'pk': self.request.user.pk})

@login_required(login_url="/login/")
def InstituicaoSedeDeleteView(request, pk):
    try:
        InstituicaoSede.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except InstituicaoSede.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('usuario:instituicao_detail_view', kwargs={'pk': request.user.pk}))