from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from apps.core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyDeleteViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import CategoriaPost, Post
from .forms import NewPostForm

class PostListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    model = Post

    def get_template_names(self):
        return [f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_list_view.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.kwargs['tipo']
        instituicao = self.kwargs['instituicao_pk']
        context["titulo"] = tipo.capitalize()
        context["tipo"] = tipo
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(categoria__nome=self.kwargs['tipo'], instituicao_id=self.kwargs['instituicao_pk'])

class PostCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    model = Post
    form_class = NewPostForm

    def get_template_names(self):
        return [f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_create_view.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        categoria = CategoriaPost.objects.get(nome=self.kwargs['tipo'])
        kwargs.update({'instituicao': self.request.user.conta, 'categoria': categoria.pk, 'user': self.request.user})
        return kwargs
    
    def get_success_url(self):
        return reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk, 'tipo': self.kwargs['tipo']})
    
class PostUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    model = Post
    form_class = NewPostForm

    def get_template_names(self):
        tipo = self.get_object().categoria.nome
        return [f'posts/{tipo}/{tipo}_create_view.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = self.get_object()
        kwargs.update({'instituicao': post.instituicao.pk, 'categoria': post.categoria.pk, 'user': post.user.pk})
        return kwargs
    
    def get_success_url(self):
        return reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})

@login_required(login_url="/login/")
def PostDeleteView(request, pk):
    try:
        Post.objects.get(pk=pk).delete()
        message_delete_registro(request)
    except Post.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': request.user.conta.pk}))