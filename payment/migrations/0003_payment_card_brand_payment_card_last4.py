# Generated by Django 5.1.6 on 2025-03-09 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='card_brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='card_last4',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
