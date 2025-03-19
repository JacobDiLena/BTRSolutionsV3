# Generated by Django 3.1.14 on 2024-08-22 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sunbiz_id', models.CharField(max_length=255)),
                ('business_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='charquestion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='floatquestion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='intquestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='BooleanQuestion',
        ),
        migrations.DeleteModel(
            name='CharQuestion',
        ),
        migrations.DeleteModel(
            name='FloatQuestion',
        ),
        migrations.DeleteModel(
            name='IntQuestion',
        ),
    ]
