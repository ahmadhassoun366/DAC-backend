# Generated by Django 4.2.4 on 2023-09-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='supcode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
