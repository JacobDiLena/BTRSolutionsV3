# Generated by Django 3.1.14 on 2024-06-15 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_item', '0005_auto_20240615_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('amount', models.FloatField(max_length=2)),
                ('pay_date', models.DateField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameModel(
            old_name='IncomeLineItem',
            new_name='FixedExpense',
        ),
        migrations.RenameModel(
            old_name='VariableExpenseLineItem',
            new_name='VariableExpense',
        ),
        migrations.DeleteModel(
            name='FixedExpenseLineItem',
        ),
        migrations.DeleteModel(
            name='LineItem',
        ),
    ]
