from django.utils import timezone
from typing import Iterable
from django.db import models
from core.models import Endereco
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
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

class Denominacao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'denominacao'

class Instituicao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)
    denominacao = models.ForeignKey(Denominacao, on_delete=models.CASCADE, null=False, blank=False)
    sigla = models.CharField(max_length=10, null=True, blank=True)
    logo = models.ImageField(max_length=100, null=False, blank=False, upload_to='instituicao/logo/')

    class Meta:
        db_table = "instituicao"

class UsuarioAbstract(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    nome = models.CharField(max_length=60, null=False, blank=False)
    celular = models.CharField(max_length=16, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Endereço")

    class Meta:
        abstract = True

class InstituicaoSede(UsuarioAbstract):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=False, blank=False, unique=True)
    sigla = models.CharField(max_length=10, null=False, blank=False)
    codigo = models.CharField(max_length=8, null=False, blank=False, unique=True)

    class Meta:
        db_table = "instituicaosede"

class Membro(UsuarioAbstract):
    sede = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    ano_ingressao = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField(null=False, blank=False)
    foto = models.ImageField(upload_to='usuario/perfil', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'membro'

    @property
    def idade(self):
        today = timezone.now().date()
        idade = int(
            today.year
            - (self.data_nascimento.year)
            - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        )
        return idade
    
    @property
    def membro_ha(self):
        today = timezone.now().date()
        membro_ha = int(
            today.year
            - (self.ano_ingressao)
        )
        return membro_ha
    
    def get_funcoes(self):
        funcoes = [str(funcao) for funcao in self.funcoes.all()]
        if funcoes:
            funcoes = " - ".join(funcoes)
            return funcoes
        return "Membro"
    
    def eventos_confirmados_pks(self):
        return self.eventos_confirmados.values_list("evento", flat=True)

class Funcao(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=True, blank=True)
    funcao = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nome da Função")
    descricao = models.TextField(null=True, blank=True, help_text="Este campo é opcional")

    def __str__(self):
        return self.funcao
     
    class Meta:
        db_table = 'funcao'

class Departamento(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nome do Departamento")
    descricao = models.TextField(null=True, blank=True, help_text="Este campo é opcional")

    def __str__(self):
        return self.departamento

    class Meta:
        db_table = 'departamento'

class FuncaoDepartamento(models.Model):
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'funcaodepartamento'

    def __str__(self):
        return f'{self.funcao} - {self.departamento}'

class FuncaoMembro(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False, related_name="funcoes")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'funcaomembro'

    def __str__(self):
        return f'{self.funcao} - {self.departamento}'