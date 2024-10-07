from typing import Iterable
from django.db import models
from core.models import Endereco
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        if self.is_admin:
            return self.conta.razao_social
        else:
            return self.conta.nome
    
    @property
    def is_admin(self):
        if hasattr(self, 'instituicaosede'):
            return True
        else:
            return False
    
    @property
    def profile_picture(self):
        if self.is_admin:
            return self.conta.instituicao.logo
        else:
            return self.conta.foto

    @property
    def conta(self):
        if self.is_admin:
            return self.instituicaosede
        else:
            return self.membro

    @property
    def instituicao(self):
        if self.is_admin:
            return self.conta
        else:
            return self.conta.sede

class Instituicao(models.Model):
    razao_social = models.CharField(max_length=120, null=False, blank=False, verbose_name="Razão Social")
    denominacao = models.CharField(max_length=120, null=False, blank=False)
    sigla = models.CharField(max_length=10, null=True, blank=True)
    logo = models.ImageField(max_length=100, null=False, blank=False, upload_to='instituicao/logo/')

    class Meta:
        db_table = "instituicao"

class InstituicaoSede(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=False, blank=False, unique=True)
    razao_social = models.CharField(max_length=120, null=False, blank=False, verbose_name="Razão Social")
    sigla = models.CharField(max_length=10, null=False, blank=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False)
    codigo = models.CharField(max_length=8, null=False, blank=False, unique=True)

    class Meta:
        db_table = "instituicaosede"

class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    nome = models.CharField(max_length=60, null=False, blank=False)
    sede = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    ano_ingressao = models.IntegerField(null=True, blank=True)
    celular = models.CharField(max_length=16, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)
    foto = models.ImageField(upload_to='usuario/perfil', max_length=255, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Endereço")

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