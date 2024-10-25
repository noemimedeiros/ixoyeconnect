from django.db import models

from agenda.models import AgendaSemanal
from evento.models import Evento
from usuario.models import InstituicaoSede, Membro

class AtividadesCulto(models.Model):
	atividade = models.CharField(max_length=80, null=False, blank=False)
	
	def __str__(self):
		return self.atividade

	class Meta:
		db_table = 'atividadesculto'

class RelatorioCulto(models.Model):
	instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False, related_name='relatorios')
	data = models.DateField(null=False, blank=False)
	hora_inicio = models.TimeField(null=False, blank=False, verbose_name='Horário Começo')
	hora_termino = models.TimeField(null=False, blank=False, verbose_name='Horário Fim')
	total_pessoas = models.IntegerField(default=0, verbose_name='Total Geral')
	total_mulheres = models.IntegerField(default=0)
	total_homens = models.IntegerField(default=0)
	total_juniores = models.IntegerField(default=0)
	total_jovens = models.IntegerField(default=0)
	total_visitantes = models.IntegerField(default=0)
	evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
	culto = models.ForeignKey(AgendaSemanal, on_delete=models.CASCADE, null=True, blank=True)
	ministro = models.CharField(max_length=100, null=True, blank=True)
	tema = models.CharField(max_length=100, null=True, blank=True, verbose_name="Mensagem/Tema")
	total_dizimos = models.DecimalField(decimal_places=2, max_digits=12, default=0, verbose_name='Total Dízimos', null=True, blank=True)
	total_ofertas = models.DecimalField(decimal_places=2, max_digits=12, default=0, null=True, blank=True)
	total_novos_convertidos = models.IntegerField(default=0)
	total_novos_batizandos = models.IntegerField(default=0)
	atividades = models.ManyToManyField(AtividadesCulto, db_table='atividadesrelatorioculto')
	
	class Meta:
		db_table = 'relatorioculto'
	
	