# Generated by Django 4.2.4 on 2023-09-30 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_changeinvacc_company_expense_managementitem_subunit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='Tva',
        ),
        migrations.CreateModel(
            name='TVA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managements', to='app1.company')),
            ],
            options={
                'verbose_name': 'TVA',
                'verbose_name_plural': 'TVAs',
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='tva',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.tva'),
        ),
        migrations.DeleteModel(
            name='Management',
        ),
    ]