from django.db import models
from django.utils import timezone
from usuario.models import FuncaoMembro, InstituicaoSede, Membro

class Escala(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False, related_name="escalas")
    funcao_membro = models.ForeignKey(FuncaoMembro, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Cargo", help_text="Selecione um membro para carregar os respectivos cargos.")
    data = models.DateField(null=False, blank=False, default=timezone.now)
    hora = models.TimeField(null=False, blank=False)

    class Meta:
        db_table = "escala"

    def __str__(self):
        return f'Escala: {self.membro} - {self.funcao_membro}'