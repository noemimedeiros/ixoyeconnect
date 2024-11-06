# Generated by Django 5.1.2 on 2024-11-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaSemanal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('dia_semana', models.CharField(choices=[('1', 'Domingo'), ('2', 'Segunda-feira'), ('3', 'Terça-feira'), ('4', 'Quarta-feira'), ('5', 'Quinta-feira'), ('6', 'Sexta-feira'), ('7', 'Sábado')], max_length=15)),
                ('hora', models.TimeField()),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agendasemanal',
            },
        ),
        migrations.CreateModel(
            name='IconeAgendaSemanal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icone_html', models.CharField(max_length=5)),
                ('icone', models.CharField(max_length=50)),
                ('descricao', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'iconeagendasemanal',
            },
        ),
    ]