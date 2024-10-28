from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from pwa_webpush import send_user_notification

from notificacao.filters import icone_notificacao
from escala.models import Escala
from posts.models import Post
from evento.models import Evento
from usuario.models import Membro
from notificacao.models import ConfiguracoesNotificacao, Notificacao

def criar_notificacao(usuario, mensagem, instance, link):
    if hasattr(usuario, 'notificacoes_configs'):
        configs = usuario.notificacoes_configs
        permitido = configs.habilitado
        if configs.silenciar_inicio and configs.silenciar_final:
            permitido = (date.today() >= configs.silenciar_final or date.today() <= configs.silenciar_final)
        if permitido:
            Notificacao.objects.create(
                user=usuario,
                mensagem=mensagem,
                id_object=instance.pk,
                modulo=instance.__class__.__name__,
                link=link
            )
    else:
        ConfiguracoesNotificacao.objects.create(user=usuario)
        Notificacao.objects.create(
            user=usuario,
            mensagem=mensagem,
            id_object=instance.pk,
            modulo=instance.__class__.__name__,
            link=link
        )

def enviar_notificacao(instance, link, mensagem, para_todos=True, usuario=None):
    icone = "static/public/img/Logo.png"
    payload = {"head": instance.__class__.__name__, "body": mensagem, "icon": icone, "link": link}

    if para_todos == False:
        criar_notificacao(usuario=usuario, instance=instance, mensagem=mensagem, link=link)
        try:
            send_user_notification(user=usuario, payload=payload, ttl=1000)
        except:
            pass
    else:
        for membro in Membro.objects.filter(sede=instance.instituicao):
            criar_notificacao(usuario=membro.user, instance=instance, mensagem=mensagem, link=link)
            try:
                send_user_notification(user=membro.user, payload=payload, ttl=1000)
            except:
                pass

@receiver(post_save, sender=Evento)
def notificar_novo_evento(sender, instance, created, **kwargs):
    if created:
        link = reverse('evento:evento_detail_view', kwargs={'pk': instance.pk})
        enviar_notificacao(instance=instance, link=link, mensagem=f"Foi publicado um novo evento: {instance.titulo}")

@receiver(post_save, sender=Post)
def notificar_novo_post(sender, instance, created, **kwargs):
    if created:
        link = reverse('posts:conteudo_detail_view', kwargs={'pk': instance.pk})
        enviar_notificacao(instance=instance, link=link, mensagem=f"Foi publicado um(a) novo(a) {instance.categoria.nome}: {instance.titulo}")

@receiver(post_save, sender=Escala)
def notificar_nova_escala(sender, instance, created, **kwargs):
    if created:
        link = reverse('escala:escala_list_view', kwargs={'instituicao_pk': instance.instituicao.pk})
        enviar_notificacao(para_todos=False, usuario=instance.membro.user, instance=instance, link=link, mensagem=f"Você foi escalado para uma nova atividade: {instance.funcao_membro}")