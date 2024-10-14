from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'usuario'

urlpatterns = [
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name="cadastrar_instituicao"),
    path('cadastrar_denominacao/', views.cadastrar_denominacao, name="cadastrar_denominacao"),
    path('cadastrar_departamento/', views.cadastrar_departamento, name="cadastrar_departamento"),
    path('cadastrar_funcao/', views.cadastrar_funcao, name="cadastrar_funcao"),

    path('membro/<int:instituicao_pk>/', views.MembroListView.as_view(), name="membro_list_view"),
    path('criar_membro/', views.MembroCreateView.as_view(), name="membro_create_view"),
    path('editar_membro/<int:pk>/', views.MembroUpdateView.as_view(), name="membro_update_view"),
    path('excluir_membro/<int:pk>/', views.MembroDeleteView, name="membro_delete_view"),

    path('funcao_por_departamento/', views.funcao_por_departamento, name="funcao_por_departamento"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
