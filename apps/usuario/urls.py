from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'usuario'

urlpatterns = [
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name="cadastrar_instituicao"),
    path('cadastrar_denominacao/', views.cadastrar_denominacao, name="cadastrar_denominacao"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
