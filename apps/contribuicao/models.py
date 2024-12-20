from django.db import models

from usuario.models import Departamento, InstituicaoSede

METODO_CONTRIBUICAO = (
    ('pix', "Pix"),
    ('deposito', "Depósito")
)
TIPO_CONTRIBUICAO = (
    ('oferta', 'Oferta'),
    ('dizimo', 'Dízimo'),
    ('doacao', 'Doação'),
    ('caridade', 'Campanhas de Caridade'),
    ('missoes', 'Contribuição para Missões'),
    ('manutencao_tempo', 'Manutenção do Templo')
)

class MetodoContribuicao(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'metodocontribuicao'

class TipoContribuicao(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'tipocontribuicao'

class Contribuicao(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False, related_name='contribuicoes')
    metodo = models.CharField(max_length=20, choices=METODO_CONTRIBUICAO, null=False, blank=False, verbose_name="Método da Contribuição")
    tipo = models.CharField(max_length=50, choices=TIPO_CONTRIBUICAO, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    chave_pix = models.CharField(max_length=100, null=True, blank=True)
    agencia = models.CharField(max_length=20, null=True, blank=True)
    conta = models.CharField(max_length=20, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.get_metodo_display()}'

    class Meta:
        db_table = 'contribuicao'

class ContatosContribuicao(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False, related_name="contatos")
    tipo = models.CharField(max_length=50, choices=TIPO_CONTRIBUICAO, null=False, blank=False)
    descricao = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=50, null=True, blank=True)
    telefone = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        db_table = 'contatoscontribuicao'

    def __str__(self):
        return f'Contatos - {self.tipo}'

    def get_contribuicao(self):
        return self.instituicao.contribuicoes.filter(tipo=self.tipo).last()