from django.db import models

from usuario.models import User
        
class Notificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    modulo = models.CharField(max_length=60, null=False, blank=False)
    mensagem = models.TextField(null=False, blank=False)
    lida = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'notificacao'

    def __str__(self):
        return f"Notificação para {self.user}"
    
class ConfiguracoesNotificacao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name="notificacoes_configs")
    habilitado = models.BooleanField(default=True, verbose_name="Habilitar/Desabilitar notificações")
    horario = models.TimeField(null=True, blank=True, verbose_name="Horário de Recebimento")
    silenciar_inicio = models.DateField(null=True, blank=True, verbose_name="Início do Período")
    silenciar_fim = models.DateField(null=True, blank=True, verbose_name="Fim do Período")

    class Meta:
        db_table = 'configuracoesnotificacao'