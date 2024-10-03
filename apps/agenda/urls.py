from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'agenda'

urlpatterns = [
    path('agendas/', views.AgendaSemanal.as_view(), name="agendas_list_view"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
