from django.db import models
from django.utils import timezone
from usuario.models import FuncaoMembro, InstituicaoSede, Membro

class StatusEscala(models.Model):
    status = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.status

    class Meta:
        db_table = "statusescala"

class Escala(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False, related_name="escalas")
    funcao_membro = models.ForeignKey(FuncaoMembro, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Cargo", help_text="Selecione um membro para carregar os respectivos cargos.")
    data = models.DateField(null=False, blank=False, default=timezone.now)
    hora = models.TimeField(null=False, blank=False)
    status = models.ForeignKey(StatusEscala, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = "escala"

    def __str__(self):
        return f'Escala: {self.membro} - {self.funcao_membro}'

class StatusTrocaSolicitada(models.Model):
    status = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.status

    class Meta:
        db_table = "statustrocasolicitada"

class TrocaSolicitada(models.Model):
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE, null=False, blank=False, related_name="escalas")
    justificativa = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey(StatusEscala, on_delete=models.CASCADE, null=False, blank=False)
    data_hora = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        db_table = "trocasolicitada"

    def __str__(self):
        return self.escala