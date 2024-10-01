# Generated by Django 5.1.1 on 2024-09-30 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denominacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
            ],
            options={
                'db_table': 'denominacao',
            },
        ),
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=8)),
                ('nome', models.CharField(max_length=120)),
                ('sigla', models.CharField(blank=True, max_length=10, null=True)),
                ('denominacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instituicao.denominacao')),
            ],
            options={
                'db_table': 'instituicao',
            },
        ),
        migrations.CreateModel(
            name='InstituicaoSede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capa', models.CharField(blank=True, max_length=255, null=True)),
                ('cnpj', models.CharField(max_length=20, unique=True)),
                ('sigla', models.CharField(max_length=10)),
                ('nome', models.CharField(max_length=120)),
                ('telefone', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.endereco')),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instituicao.instituicao')),
            ],
            options={
                'db_table': 'instituicaosede',
            },
        ),
    ]
