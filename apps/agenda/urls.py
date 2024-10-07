from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'agenda'

urlpatterns = [
    path('agendas/<int:instituicao_pk>/', views.AgendaSemanalListView.as_view(), name="agendas_list_view"),
    path('criar_agenda/', views.AgendaSemanalCreateView.as_view(), name="agendas_create_view"),
    path('editar_agenda/<int:pk>/', views.AgendaSemanalUpdateView.as_view(), name="agendas_update_view"),
    path('excluir_agenda/<int:pk>/', views.AgendaSemanalDeleteView, name="agendas_delete_view")
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
