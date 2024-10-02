from django.db import models
from django.contrib.auth.models import User
from core.models import Endereco

class Denominacao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)

    class Meta:
        db_table = "denominacao"

class Instituicao(models.Model):
    denominacao = models.ForeignKey(Denominacao, on_delete=models.CASCADE, null=False, blank=False)
    logo = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=8, null=False, blank=False)
    razao_social = models.CharField(max_length=120, null=False, blank=False, verbose_name="Razão Social")
    sigla = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "instituicao"

class InstituicaoSede(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=False, blank=False, unique=True)
    razao_social = models.CharField(max_length=120, null=False, blank=False, verbose_name="Razão Social")
    sigla = models.CharField(max_length=10, null=False, blank=False)
    telefone = models.CharField(max_length=16, null=False, blank=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False)
    capa = models.ImageField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "instituicaosede"