# Generated by Django 5.0.7 on 2024-09-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
