# Generated by Django 5.1 on 2024-09-08 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalfinancials',
            old_name='current_liabilities',
            new_name='liabilities',
        ),
    ]
