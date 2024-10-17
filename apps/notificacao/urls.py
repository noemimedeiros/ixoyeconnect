from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'notificacao'

urlpatterns = [
    path('notificacoes/', views.NotificacaoListView.as_view(), name="notificacoes_list_view"),
    path('minha_conta/notificacoes_configurar/', views.ConfiguracoesNotificacaoView.as_view(), name="notificacoes_configurar"),
    path('excluir_notificacao/<int:pk>/', views.NotificacaoDeleteView, name="notificacao_delete_view"),

    path('ler_notificacao/', views.ler_notificacao, name="ler_notificacao"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)