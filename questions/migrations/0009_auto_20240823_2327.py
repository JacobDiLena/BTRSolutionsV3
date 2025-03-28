# Generated by Django 3.1.14 on 2024-08-24 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20240823_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='avg_inventory',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='business',
            name='sqft',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='business',
            name='wholesale_retail',
            field=models.CharField(choices=[('Wholesale', 'Wholesale'), ('Retail', 'Retail'), ('N/A', 'N/A')], default='N/A', max_length=255),
        ),
    ]
