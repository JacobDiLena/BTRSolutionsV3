# Generated by Django 3.1.14 on 2024-08-28 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0014_auto_20240827_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='Unique_ID',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
