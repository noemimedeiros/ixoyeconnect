from django.db import models

from usuario.models import Instituicao, Departamento

class MetodoContribuicao(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'metodocontribuicao'

class TipoContribuicao(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'tipocontribuicao'

class Contribuicao(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    metodo = models.ForeignKey(MetodoContribuicao, on_delete=models.CASCADE, null=False, blank=False)
    tipo = models.ForeignKey(TipoContribuicao, on_delete=models.CASCADE, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)
    chave_pix = models.CharField(max_length=100, null=True, blank=True)
    agencia = models.CharField(max_length=20, null=True, blank=True)
    conta = models.CharField(max_length=20, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'contribuicao'

class ContatosContribuicao(models.Model):
    contribuicao = models.ForeignKey(Contribuicao, on_delete=models.CASCADE, null=False, blank=False)
    email = models.CharField(max_length=50, null=True, blank=True)
    telefone = models.CharField(max_length=16, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'contatoscontribuicao'