from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'escala'

urlpatterns = [
    path('escala/<int:instituicao_pk>/', views.EscalaListView.as_view(), name="escala_list_view"),
    path('criar_escala/<int:instituicao_pk>/', views.criar_escala, name="escala_create_view"),
    path('editar_escala/<int:pk>/', views.editar_escala, name="escala_update_view"),
    path('excluir_escala/<int:pk>/', views.excluir_escala, name="escala_delete_view"),

    path('funcoes_por_membro/', views.funcoes_por_membro, name="funcoes_por_membro"),
    path('carregar_infos_editar/', views.carregar_infos_editar, name="carregar_infos_editar"),
    path('confirmar_escala/<int:pk>/', views.confirmar_escala, name="confirmar_escala"),
    path('solicitar_troca_escala/<int:pk>/', views.solicitar_troca_escala, name="solicitar_troca_escala"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
