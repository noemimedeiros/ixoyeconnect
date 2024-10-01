from django.db import models

from django.utils import timezone

from membro.models import Membro
from core.models import Endereco
from instituicao.models import Instituicao

class Evento(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    data = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True)

    class Meta:
        db_table = "evento"

class ParticipanteEvento(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=False)
    data_ingressao = models.DateField(null=False, blank=False, default=timezone.now)

    class Meta:
        db_table = "participanteevento"