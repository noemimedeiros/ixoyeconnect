# Generated by Django 5.1.2 on 2024-11-06 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracoesNotificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habilitado', models.BooleanField(default=True, verbose_name='Habilitar/Desabilitar notificações')),
                ('horario', models.TimeField(blank=True, null=True, verbose_name='Horário de Recebimento')),
                ('silenciar_inicio', models.DateField(blank=True, null=True, verbose_name='Início do Período')),
                ('silenciar_fim', models.DateField(blank=True, null=True, verbose_name='Fim do Período')),
            ],
            options={
                'db_table': 'configuracoesnotificacao',
            },
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.CharField(max_length=60)),
                ('id_object', models.IntegerField()),
                ('mensagem', models.TextField()),
                ('lida', models.BooleanField(default=False)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'notificacao',
            },
        ),
    ]
