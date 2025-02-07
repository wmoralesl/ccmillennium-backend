# Generated by Django 5.0.7 on 2024-10-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_enrollment_description_and_more'),
        ('payments', '0004_alter_payment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('enrollment', 'month_paid')},
        ),
        migrations.AlterField(
            model_name='payment',
            name='month_paid',
            field=models.PositiveIntegerField(),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_sequence',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
    ]
