# Generated by Django 5.0.7 on 2024-09-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='courses'),
        ),
    ]
