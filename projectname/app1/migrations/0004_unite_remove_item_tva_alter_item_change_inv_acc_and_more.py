# Generated by Django 4.2.4 on 2023-09-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_compnay_management_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Unite',
                'verbose_name_plural': 'Unites',
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='TVA',
        ),
        migrations.AlterField(
            model_name='item',
            name='change_inv_acc',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='expense',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='purchase',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='revenue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='tva',
            field=models.FloatField(blank=True, choices=[('0.1', '10%'), ('0.05', '5%'), ('0.0', '0%')], default='0.0', null=True),
        ),
    ]
