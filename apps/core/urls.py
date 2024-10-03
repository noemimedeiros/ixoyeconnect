from django.urls import path
from django.conf.urls.static import static
from django.urls import path

from ixoyeconnect import settings

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.DashboradView.as_view(), name='dashboard'),
    path('signup/', views.MyCadastroView.as_view(), name="signup_url"),
    path('login/', views.MyLoginView.as_view(), name="account_login"),
] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
