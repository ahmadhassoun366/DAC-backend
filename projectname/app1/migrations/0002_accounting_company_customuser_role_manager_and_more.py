# Generated by Django 4.2.4 on 2023-09-18 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('purchase', models.FloatField(blank=True, null=True)),
                ('expense', models.FloatField(blank=True, null=True)),
                ('change_inv_acc', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/company_images')),
                ('name', models.CharField(max_length=200)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('taxIdentification', models.CharField(blank=True, max_length=20, null=True)),
                ('commercialRegister', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('Address', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('company', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=30, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manager',
                'verbose_name_plural': 'Managers',
            },
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TVA', models.FloatField(blank=True, null=True)),
                ('compnay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managements', to='app1.company')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supcode', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('TTC', models.FloatField(blank=True, null=True)),
                ('place', models.CharField(blank=True, max_length=200, null=True)),
                ('addValueCost', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, null=True)),
                ('final_good', models.CharField(choices=[('start', 'Start'), ('mid', 'Mid'), ('finish', 'Finished')], default='finished', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/item_images')),
                ('minimum_quantity', models.IntegerField(blank=True, null=True)),
                ('TVA', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.management')),
                ('change_inv_acc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='change_inv_acc_item', to='app1.accounting')),
                ('expense', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_item', to='app1.accounting')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app1.manager')),
                ('purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_item', to='app1.accounting')),
                ('revenue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='revenue_item', to='app1.accounting')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='app1.manager'),
        ),
        migrations.AddField(
            model_name='accounting',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountings', to='app1.company'),
        ),
    ]