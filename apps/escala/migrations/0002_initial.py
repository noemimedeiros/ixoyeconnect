# Generated by Django 5.1.3 on 2024-11-05 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escala', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='escala',
            name='funcao_membro',
            field=models.ForeignKey(help_text='Selecione um membro para carregar os respectivos cargos.', on_delete=django.db.models.deletion.CASCADE, to='usuario.funcaomembro', verbose_name='Cargo'),
        ),
        migrations.AddField(
            model_name='escala',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.instituicaosede'),
        ),
        migrations.AddField(
            model_name='escala',
            name='membro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escalas', to='usuario.membro'),
        ),
    ]
