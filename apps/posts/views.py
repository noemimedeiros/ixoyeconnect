from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse

from apps.core.messages_utils import message_delete_registro, message_error_registro
from core.views import MyCreateViewIxoyeConnect, MyDeleteViewIxoyeConnect, MyUpdateViewIxoyeConnect, MyListViewIxoyeConnect

from .models import Post
from .forms import NewPostForm

class PostListView(LoginRequiredMixin, MyListViewIxoyeConnect):
    model = Post

    def get_template_names(self):
        return [f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_list_view.html']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(categoria__nome=self.kwargs['tipo'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostCreateView(LoginRequiredMixin, MyCreateViewIxoyeConnect):
    model = Post
    form_class = NewPostForm

    def get_template_names(self):
        return [f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_create_view.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
        return kwargs
    
    def get_success_url(self):
        return reverse('posts:conteudo_list_view', kwargs={'instituicao_pk': self.request.user.conta.pk})
    
class PostUpdateView(LoginRequiredMixin, MyUpdateViewIxoyeConnect):
    model = Post
    form_class = NewPostForm

    def get_template_names(self):
        return [f'posts/{self.kwargs['tipo']}/{self.kwargs['tipo']}_create_view.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instituicao': self.request.user.conta})
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