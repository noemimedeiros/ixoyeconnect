from django.db import models

from instituicao.models import Instituicao

class AgendaSemanal(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    dia_semana = models.CharField(max_length=15, null=False, blank=False)
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    icone = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "agendasemanal"