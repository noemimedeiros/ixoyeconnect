from django.db import models

class UnidadeFederativa(models.Model):
    sigla = models.CharField(max_length=2, null=False, blank=False)
    uf = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'{self.uf}'

    class Meta:
        db_table = 'unidadefederativa'

class Endereco(models.Model):
    uf = models.ForeignKey(UnidadeFederativa, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Unidade Federativa")
    cidade = models.CharField(max_length=60, null=False, blank=False)
    bairro = models.CharField(max_length=60, null=False, blank=False)
    rua = models.CharField(max_length=60, null=False, blank=False)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    numero = models.IntegerField(null=False, blank=False)
    cep = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.complemento}, {self.bairro}, {self.cidade} - {self.uf.sigla}'

    class Meta:
        db_table = 'endereco'

