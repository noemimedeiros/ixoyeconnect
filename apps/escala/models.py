from django.db import models

from usuario.models import FuncaoMembro

class Escala(models.Model):
    data = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    funcao_membro = models.ForeignKey(FuncaoMembro, on_delete=models.CASCADE, null=False, blank=False)