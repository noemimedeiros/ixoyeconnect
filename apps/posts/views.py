import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.template.loader import get_template

from apps.core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyDetailViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect
from ixoyeconnect import settings

from .models import ArquivoPost, CategoriaPost, Curtida, Post, Salvo
from .forms import ArquivoPostForm, ArquivoPostFormSet, NewPostForm

class PostListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    model = Post
    ordering = ['-data', '-hora']
    search_fields =  ['titulo', 'descricao']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.template_name = f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_list_view.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            self.template_name = 'posts/base/base_list.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.kwargs['tipo']
        instituicao = self.kwargs['instituicao_pk']
        context["titulo"] = tipo.capitalize()
        context["tipo"] = tipo
        context["active"] = ["conteudo", tipo]
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(categoria__nome=self.kwargs['tipo'], instituicao_id=self.kwargs['instituicao_pk'])
        return qs
    

class PostCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    model = Post
    form_class = NewPostForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.template_name = f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_create_view.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            self.template_name = 'posts/base/base_create.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.kwargs['tipo']
        context["titulo"] = f'Criar {tipo}'
        context["arquivos_formset"] = ArquivoPostFormSet()
        context["active"] = ["conteudo", tipo]
        return context
    
    def form_valid(self, form):
        form = form.save()
        arquivos_formset = ArquivoPostFormSet(self.request.POST, self.request.FILES)
        arquivos = arquivos_formset.save(commit=False)
        for arquivo in arquivos:
            arquivo.post = form
            arquivo.nome
            arquivo.save()
        return HttpResponseRedirect(self.get_success_url())
    
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

    def dispatch(self, request, *args, **kwargs):
        tipo = self.get_object().categoria.nome
        try:
            self.template_name = f'posts/{tipo}/{tipo}_create_view.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            self.template_name = 'posts/base/base_create.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.get_object().categoria.nome
        context["titulo"] = f'Editar {tipo}'
        context["active"] = ["conteudo", tipo]
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = self.get_object()
        kwargs.update({'instituicao': post.instituicao.pk, 'categoria': post.categoria.pk, 'user': post.user.pk})
        return kwargs
    
    def get_success_url(self):
        tipo = self.get_object().categoria.nome
        return reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk, 'tipo': tipo})

class PostDetailView(LoginRequiredMixin, MyDetailViewIxoyeConnect):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        tipo = self.get_object().categoria.nome
        try:
            self.template_name = f'posts/{tipo}/{tipo}_detail_view.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            self.template_name = 'posts/base/base_detail.html'
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["titulo"] = post.titulo
        context["active"] = ["conteudo", post.categoria.nome]
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = self.get_object()
        kwargs.update({'instituicao': post.instituicao.pk, 'categoria': post.categoria.pk, 'user': post.user.pk})
        return kwargs

@login_required(login_url="/login/")
def PostDeleteView(request, pk):
    post = Post.objects.get(pk=pk)
    tipo = post.categoria.nome
    try:
        post.delete()
        message_delete_registro(request)
    except Post.DoesNotExist:
        message_error_registro(request)
    return HttpResponseRedirect(reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': request.user.conta.pk, 'tipo': tipo}))

@login_required(login_url='/login/')
def curtir_post(request, user, post):
    curtido = False
    try:
        Curtida.objects.create(user_id=user, post_id=post)
        curtido = True
    except:
        Curtida.objects.get(user_id=user, post_id=post).delete()
        curtido = False
    return JsonResponse(curtido, safe=False)

@login_required(login_url='/login/')
def salvar_post(request, user, post):
    salvo = False
    try:
        Salvo.objects.create(user_id=user, post_id=post)
        salvo = True
    except:
        Salvo.objects.get(user_id=user, post_id=post).delete()
        salvo = False
    return JsonResponse(salvo, safe=False)