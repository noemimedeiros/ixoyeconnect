from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'relatorio'

urlpatterns = [
    path('relatorio/<int:instituicao_pk>/', views.RelatorioCultoListView.as_view(), name="relatorio_list_view"),
    path('criar_relatorio/', views.RelatorioCultoCreateView.as_view(), name="relatorio_create_view"),
    path('editar_relatorio/<int:pk>/', views.RelatorioCultoUpdateView.as_view(), name="relatorio_update_view"),
    path('excluir_relatorio/<int:pk>/', views.RelatorioCultoDeleteView, name="relatorio_delete_view"),

    path('imprimir_relatorio/<int:instituicao_pk>/', views.RelatorioImprimir, name="imprimir_relatorio")
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
