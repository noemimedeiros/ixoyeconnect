from django.db import models

from usuario.models import InstituicaoSede

DIAS_SEMANA = (
    ('1', 'Domingo'),
    ('2', 'Segunda-feira'),
    ('3', 'Terça-feira'),
    ('4', 'Quarta-feira'),
    ('5', 'Quinta-feira'),
    ('6', 'Sexta-feira'),
    ('7', 'Sábado')
)

class IconeAgendaSemanal(models.Model):
    icone_html = models.CharField(max_length=5, null=False, blank=False)
    icone = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "iconeagendasemanal"
    
    def __str__(self):
        return self.descricao

class AgendaSemanal(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False, related_name="agendas_semanais")
    titulo = models.CharField(max_length=50, null=False, blank=False)
    dia_semana = models.CharField(choices=DIAS_SEMANA, max_length=15, null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    icone = models.ForeignKey(IconeAgendaSemanal, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.get_dia_semana_display()} - {self.titulo}'

    class Meta:
        db_table = "agendasemanal"