# Generated by Django 5.1.2 on 2024-10-17 00:42

import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'categoriapost',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capa', models.ImageField(blank=True, max_length=255, null=True, upload_to='posts/capa/')),
                ('fixado', models.BooleanField(default=False, verbose_name='Deseja fixar esse post?')),
                ('titulo', models.CharField(max_length=50)),
                ('descricao', django_ckeditor_5.fields.CKEditor5Field()),
                ('hora', models.TimeField(auto_now=True)),
                ('data', models.DateField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.categoriapost')),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.instituicaosede')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='ArquivoPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(max_length=255, upload_to='posts/arquivos/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='posts.post')),
            ],
            options={
                'db_table': 'arquivopost',
            },
        ),
        migrations.CreateModel(
            name='Curtida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curtidas', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curtida', to='posts.post')),
            ],
            options={
                'db_table': 'curtida',
                'constraints': [models.UniqueConstraint(fields=('post', 'user'), name='un_post_user_curitda')],
            },
        ),
        migrations.CreateModel(
            name='Salvo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salvo', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salvos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'salvo',
                'constraints': [models.UniqueConstraint(fields=('post', 'user'), name='un_post_user_salvo')],
            },
        ),
    ]
