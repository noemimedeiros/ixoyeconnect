from django.db import models

from core.models import Endereco

class Usuario(models.Model):
    foto = models.ImageField(upload_to='usuario/perfil', max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=16, null=False, blank=False)
    nome = models.CharField(max_length=60, null=False, blank=False)
    idade = models.IntegerField(null=False, blank=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Endereço")
    data_nascimento = models.DateField(null=False, blank=False)

    class Meta:
        db_table = "usuario"