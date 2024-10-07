from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'usuario'

urlpatterns = [
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name="cadastrar_instituicao"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
