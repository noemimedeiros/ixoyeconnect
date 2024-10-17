from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from .views import views, views_membro, views_instituicao

app_name = 'usuario'

urlpatterns = [
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name="cadastrar_instituicao"),
    path('cadastrar_denominacao/', views.cadastrar_denominacao, name="cadastrar_denominacao"),
    path('cadastrar_departamento/', views.cadastrar_departamento, name="cadastrar_departamento"),
    path('cadastrar_funcao/', views.cadastrar_funcao, name="cadastrar_funcao"),

    # Membro
    path('membro/meu_perfil/<int:pk>/', views_membro.MembroDetailView.as_view(), name="membro_detail_view"),
    path('membros/<int:instituicao_pk>/', views_membro.MembroListView.as_view(), name="membro_list_view"),
    path('criar_membro/', views_membro.MembroCreateView.as_view(), name="membro_create_view"),
    path('editar_membro/<int:pk>/', views_membro.MembroUpdateView.as_view(), name="membro_update_view"),
    path('editar_perfil_membro/<int:pk>/', views_membro.MembroProfileUpdateView.as_view(), name="membro_update_profile_view"),
    path('excluir_membro/<int:pk>/', views_membro.MembroDeleteView, name="membro_delete_view"),

    path('funcao_por_departamento/', views_membro.funcao_por_departamento, name="funcao_por_departamento"),
    path('devincular_usuario/<int:membro_pk>/', views_membro.devincular_usuario, name="devincular_usuario"),

    # Instituição
    path('instituicao/<int:pk>/', views_instituicao.InstituicaoSedeDetailView.as_view(), name="instituicao_detail_view"),
    path('editar_instituicao/<int:pk>/', views_instituicao.InstituicaoSedeUpdateView.as_view(), name="instituicao_update_view"),
    path('excluir_instituicao/<int:pk>/', views_instituicao.InstituicaoSedeDeleteView, name="instituicao_delete_view"),

    # Perfil
    path('meu_perfil/', views.MeuPerfilView.as_view(), name="meu_perfil"),
    path('minha_conta/senha_seguranca/', views.SenhaSegurancaView.as_view(), name="senha_seguranca"),
    path('minha_conta/deletar_conta/', views.DeletarContaView.as_view(), name="deletar_conta"),
    
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
