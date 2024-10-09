from django.db import models

from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from usuario.models import Membro, InstituicaoSede
from core.models import Endereco

class Evento(models.Model):
    capa = models.ImageField(upload_to='posts/capa/',max_length=255, null=True, blank=True)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    descricao = CKEditor5Field(null=True, blank=True)
    valor = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, help_text="Para que o evento seja considerado gratuito, basta deixar o campo de valor em branco.")
    data = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = "evento"

class ParticipanteEvento(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=False, related_name="participantes")
    data_ingressao = models.DateField(null=False, blank=False, default=timezone.now)

    class Meta:
        db_table = "participanteevento"