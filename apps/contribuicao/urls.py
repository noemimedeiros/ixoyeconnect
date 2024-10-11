from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'contribuicao'

urlpatterns = [
    path('contribuicao/<int:instituicao_pk>/', views.ContribuicaoListView.as_view(), name="contribuicao_list_view"),
    path('criar_contribuicao/', views.ContribuicaoCreateView.as_view(), name="contribuicao_create_view"),
    path('editar_contribuicao/<int:pk>/', views.ContribuicaoUpdateView.as_view(), name="contribuicao_update_view"),
    path('excluir_contribuicao/<int:pk>/', views.ContribuicaoDeleteView, name="contribuicao_delete_view"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
