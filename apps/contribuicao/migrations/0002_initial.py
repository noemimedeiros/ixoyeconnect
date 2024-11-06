# Generated by Django 5.1.2 on 2024-11-06 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contribuicao', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contatoscontribuicao',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contatos', to='usuario.instituicaosede'),
        ),
        migrations.AddField(
            model_name='contribuicao',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.departamento'),
        ),
        migrations.AddField(
            model_name='contribuicao',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contribuicoes', to='usuario.instituicaosede'),
        ),
    ]
