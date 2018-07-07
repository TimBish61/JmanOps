# Generated by Django 2.0.4 on 2018-06-10 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180608_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllPaymentAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('ContactNumber', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CurrencyCode', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Type', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('ObjectID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('ObjectNumber', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('PaymentID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('RowUpdated', models.DateTimeField(auto_now=True)),
                ('RowInserted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='xeroallpaymentanalysis',
            unique_together={('ObjectID', 'PaymentID')},
        ),
    ]
