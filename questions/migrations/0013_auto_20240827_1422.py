# Generated by Django 3.1.14 on 2024-08-27 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_auto_20240827_1216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='Status',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='business',
            name='Filing Type',
        ),
    ]
