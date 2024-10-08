from django.db import models
from usuario.models import User, InstituicaoSede
from django_ckeditor_5.fields import CKEditor5Field

class CategoriaPost(models.Model):
    nome = models.CharField(max_length=50 , null=False, blank=False)

    class Meta:
        db_table = 'categoriapost'

    def __str__(self):
        return self.nome

class Post(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    capa = models.ImageField(upload_to='posts/capa/',max_length=255, null=True, blank=True)
    fixado = models.BooleanField(default=False, verbose_name="Deseja fixar esse post?")
    titulo = models.CharField(max_length=50, null=False, blank=False)
    descricao = CKEditor5Field(null=True, blank=True)
    hora = models.TimeField(null=False, blank=False, auto_now=True)
    data = models.DateField(null=False, blank=False, auto_now=True)
    categoria = models.ForeignKey(CategoriaPost, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'post'

class ArquivoPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    arquivo = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'arquivopost'

class Salvo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'salvo'

class Curtida(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'curtida'