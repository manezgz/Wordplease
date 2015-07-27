# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=80)),
                ('resumen', models.CharField(max_length=500)),
                ('urlImage', models.URLField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('categorias', models.CharField(max_length=4, choices=[(b'TECH', b'Tecnologia'), (b'LIBR', b'Libros'), (b'VGAM', b'Videojuegos')])),
            ],
        ),
    ]
