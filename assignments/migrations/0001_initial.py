# Generated by Django 5.0.7 on 2024-10-21 20:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0012_rename_mount_enrollment_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.group')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('graded', models.BooleanField(default=False)),
                ('grade', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignments.assignment')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
