from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'posts'

urlpatterns = [
    path('conteudo/<str:tipo>/<int:instituicao_pk>/', views.PostListView.as_view(), name="conteudo_list_view"),
    path('criar_conteudo/<str:tipo>/<int:instituicao_pk>/', views.PostCreateView.as_view(), name="conteudo_create_view"),
    path('editar_conteudo/<int:pk>/', views.PostUpdateView.as_view(), name="conteudo_update_view"),
    path('excluir_conteudo/<int:pk>/', views.PostDeleteView, name="conteudo_delete_view"),
    path('ver_conteudo/<int:pk>/', views.PostDetailView.as_view(), name="conteudo_detail_view")
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
