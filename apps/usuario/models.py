from django.db import models
from django.contrib.auth.models import User

from core.models import Endereco

class Usuario(models.Model):
    user = models.OneToOneField(User, related_name='usuario_user', on_delete=models.CASCADE, null=False, blank=False)
    nome = models.CharField(max_length=60, null=False, blank=False)
    celular = models.CharField(max_length=16, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)
    foto = models.ImageField(upload_to='usuario/perfil', max_length=255, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Endereço")

    class Meta:
        db_table = "usuario"