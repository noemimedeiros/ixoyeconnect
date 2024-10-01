from django.db import models

from instituicao.models import InstituicaoSede
from usuario.models import Usuario

class Membro(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, blank=False)
    sede = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    ano_ingressao = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'membro'

class Funcao(models.Model):
    funcao = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
     
    class Meta:
        db_table = 'funcao'

class Departamento(models.Model):
    departamento = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'departamento'

class FuncaoMembro(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False)
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'funcaomembro'