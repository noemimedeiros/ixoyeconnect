# Generated by Django 5.1.2 on 2024-10-17 00:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=django.utils.timezone.now)),
                ('hora', models.TimeField()),
                ('funcao_membro', models.ForeignKey(help_text='Selecione um membro para carregar os respectivos cargos.', on_delete=django.db.models.deletion.CASCADE, to='usuario.funcaomembro', verbose_name='Cargo')),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.instituicaosede')),
                ('membro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.membro')),
            ],
            options={
                'db_table': 'escala',
            },
        ),
    ]
