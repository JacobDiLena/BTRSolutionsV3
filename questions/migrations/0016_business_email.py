# Generated by Django 3.1.14 on 2024-08-28 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_business_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='email',
            field=models.EmailField(default='Enter Email Here', help_text='Enter the email you would like communication sent to', max_length=254),
        ),
    ]
