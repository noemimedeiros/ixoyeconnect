from celery import shared_task
from pwa_webpush import send_user_notification
from datetime import date

from notificacao.models import ConfiguracoesNotificacao, Notificacao

@shared_task
def notificacao_push_task(notificacao_id):
    try:
        notificacao = Notificacao.objects.get(pk=notificacao_id)
    except Notificacao.DoesNotExist:
        print(f"Erro ao gerar notificação push.")
        return
        
    usuario = notificacao.user
    permitido = True
    if not hasattr(usuario, 'notificacoes_configs'):
        ConfiguracoesNotificacao.objects.create(user=usuario)
    else:
        configs = usuario.notificacoes_configs
        permitido = configs.habilitado
        if configs.silenciar_inicio and configs.silenciar_final:
            permitido = (date.today() >= configs.silenciar_final or date.today() <= configs.silenciar_final)
    
    icone = "static/public/img/Logo.png"
    payload = {"head": notificacao.modulo, "body": notificacao.mensagem, "icon": icone, "link": notificacao.link}
    
    if permitido:
        try:
            send_user_notification(user=notificacao.user, payload=payload, ttl=1000)
        except Exception as e:
            print(f"Não foi possível enviar a notificação push: {e}")