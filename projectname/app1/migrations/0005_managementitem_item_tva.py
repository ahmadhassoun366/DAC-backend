# Generated by Django 4.2.4 on 2023-09-24 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_unit_amount_unit_operation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tva', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='Tva',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.management'),
        ),
    ]