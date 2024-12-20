from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', 'core'), name="core"),
    path('', include('allauth.urls')),
    path('', include('agenda.urls')),
    path('usuario/', include('usuario.urls')),
    path('', include('posts.urls')),
    path('', include('evento.urls')),
    path('', include('contribuicao.urls')),
    path('', include('escala.urls')),
    path('', include('notificacao.urls')),
    path('', include('relatorios.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path(r'', include('pwa.urls')),
    path('webpush/', include('webpush.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()