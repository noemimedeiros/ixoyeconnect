from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'evento'

urlpatterns = [
    path('evento/<int:instituicao_pk>/', views.EventoListView.as_view(), name="evento_list_view"),
    path('criar_evento/', views.EventoCreateView.as_view(), name="evento_create_view"),
    path('editar_evento/<int:pk>/', views.EventoUpdateView.as_view(), name="evento_update_view"),
    path('excluir_evento/<int:pk>/', views.EventoDeleteView, name="evento_delete_view"),
    path('ver_evento/<int:pk>/', views.EventoDetailView.as_view(), name="evento_detail_view")
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
