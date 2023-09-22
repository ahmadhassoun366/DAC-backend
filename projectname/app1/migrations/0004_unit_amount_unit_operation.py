# Generated by Django 4.2.4 on 2023-09-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_item_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='operation',
            field=models.CharField(blank=True, choices=[('*', 'Multiplication'), ('/', 'Division'), ('+', 'Addition'), ('-', 'Substraction')], max_length=1, null=True),
        ),
    ]
