from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'contribuicao'

urlpatterns = [
    path('contribuicao/<int:instituicao_pk>/', views.contribuicaoListView.as_view(), name="contribuicao_list_view"),
    path('criar_contribuicao/', views.contribuicaoCreateView.as_view(), name="contribuicao_create_view"),
    path('editar_contribuicao/<int:pk>/', views.contribuicaoUpdateView.as_view(), name="contribuicao_update_view"),
    path('excluir_contribuicao/<int:pk>/', views.contribuicaoDeleteView, name="contribuicao_delete_view"),
    path('ver_contribuicao/<int:pk>/', views.contribuicaoDetailView.as_view(), name="contribuicao_detail_view")
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
