# Generated by Django 3.1.14 on 2024-06-17 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_item', '0013_auto_20240617_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
