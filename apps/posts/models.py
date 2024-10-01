from django.db import models

from usuario.models import Usuario
from instituicao.models import Instituicao

class CategoriaPost(models.Model):
    nome = models.CharField(max_length=50 , null=False, blank=False)

    class Meta:
        db_table = 'categoriapost'

class Post(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    descricao =  models.TextField(null=True, blank=True)
    capa = models.CharField(max_length=255, null=True, blank=True)
    hora = models.TimeField(null=False, blank=False)
    data = models.DateField(null=False, blank=False)
    categoria = models.ForeignKey(CategoriaPost, on_delete=models.CASCADE, null=False, blank=False)
    fixado = models.BooleanField(default=0)

    class Meta:
        db_table = 'post'

class ArquivoPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    arquivo = models.CharField(max_length=255, null=False, blank=False)

     
    class Meta:
        db_table = 'arquivopost'

class Salvo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'salvo'

class Curtida(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'curtida'