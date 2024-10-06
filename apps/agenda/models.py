from django.db import models
from django.utils.safestring import mark_safe

from instituicao.models import Instituicao

class IconeAgendaSemanal(models.Model):
    icone_html = models.CharField(max_length=5, null=False, blank=False)
    icone = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "iconeagendasemanal"
    
    def __str__(self):
        return self.descricao

class AgendaSemanal(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    dia_semana = models.CharField(max_length=15, null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    icone = models.ForeignKey(IconeAgendaSemanal, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "agendasemanal"