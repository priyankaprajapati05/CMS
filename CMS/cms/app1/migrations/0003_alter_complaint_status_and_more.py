# Generated by Django 5.0.7 on 2025-03-25 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_resolvedcomplaint_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='resolvedcomplaint',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], max_length=50),
        ),
    ]
