# Generated by Django 5.1.1 on 2024-09-30 22:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('instituicao', '0001_initial'),
        ('membro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.endereco')),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instituicao.instituicao')),
            ],
            options={
                'db_table': 'evento',
            },
        ),
        migrations.CreateModel(
            name='ParticipanteEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ingressao', models.DateField(default=django.utils.timezone.now)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evento.evento')),
                ('membro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membro.membro')),
            ],
            options={
                'db_table': 'participanteevento',
            },
        ),
    ]
