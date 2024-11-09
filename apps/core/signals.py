from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from webpush import send_user_notification
from concurrent.futures import ThreadPoolExecutor

from notificacao.filters import icone_notificacao
from escala.models import Escala
from posts.models import Post
from evento.models import Evento
from usuario.models import Membro
from notificacao.models import ConfiguracoesNotificacao, Notificacao

executor = ThreadPoolExecutor(max_workers=5)

def notificacao_push_async(notificacao_id):
    notificacao = Notificacao.objects.get(pk=notificacao_id)
    icone = "static/public/img/Logo.png"
    payload = {"head": notificacao.modulo, "body": notificacao.mensagem, "icon": icone, "link": notificacao.link}
    if hasattr(notificacao.user, 'notificacoes_configs'):
        configs = notificacao.user.notificacoes_configs
        permitido = configs.habilitado
        if configs.silenciar_inicio and configs.silenciar_final:
            permitido = (date.today() >= configs.silenciar_final or date.today() <= configs.silenciar_final)
        if not permitido:
            return 
    else:
        ConfiguracoesNotificacao.objects.create(user=notificacao.user)
    try:
        send_user_notification(user=notificacao.user, payload=payload, ttl=100)
    except:
        pass

@receiver(post_save, sender=Notificacao)
def criar_notificacao_push(sender, instance, created, **kwargs):
    if created:
        executor.submit(notificacao_push_async, instance.pk)

def enviar_notificacao(instance, link, mensagem, para_todos=True, usuario=None):
    if para_todos == False:
        Notificacao.objects.create(
            user=instance.membro.user,
            mensagem=mensagem,
            id_object=instance.pk,
            modulo=instance.__class__.__name__,
            link=link
        )
    else:
        for membro in Membro.objects.filter(sede=instance.instituicao):
            Notificacao.objects.create(
                user=membro.user,
                mensagem=mensagem,
                id_object=instance.pk,
                modulo=instance.__class__.__name__,
                link=link
            )

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