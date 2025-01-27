# Generated by Django 5.0.7 on 2024-08-20 20:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('año', models.PositiveIntegerField()),
                ('presencial', models.BooleanField(default=True)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('horario', models.TimeField()),
                ('cant_horas', models.PositiveIntegerField()),
                ('visible', models.BooleanField(default=True)),
                ('activo', models.BooleanField(default=True)),
                ('idCurso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course')),
                ('profesor', models.ForeignKey(blank=True, limit_choices_to={'role': 'teacher'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'ordering': ['inicio'],
            },
        ),
    ]
