# Generated by Django 2.0.4 on 2018-06-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_xeroalltaxrates'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(blank=True, default='', max_length=30, unique=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100)),
                ('Type', models.CharField(blank=True, default='', max_length=20)),
                ('BankAccountNumber', models.CharField(blank=True, default='', max_length=30)),
                ('Status', models.CharField(blank=True, default='', max_length=20)),
                ('Description', models.CharField(blank=True, default='', max_length=100)),
                ('BankAccountType', models.CharField(blank=True, default='', max_length=20)),
                ('CurrencyCode', models.CharField(blank=True, default='', max_length=4)),
                ('TaxType', models.CharField(blank=True, default='', max_length=20)),
                ('EnablePaymentsToAccount', models.BooleanField(default=False)),
                ('ShowInExpenseClaims', models.BooleanField(default=False)),
                ('AccountID', models.CharField(blank=True, default='', max_length=64, unique=True)),
                ('Class', models.CharField(blank=True, default='', max_length=20)),
                ('SystemAccount', models.BooleanField(default=False)),
                ('ReportingCode', models.CharField(blank=True, default='', max_length=100)),
                ('ReportingCodeName', models.CharField(blank=True, default='', max_length=100)),
                ('HasAttachments', models.BooleanField(default=False)),
                ('UpdatedDateUTC', models.DateTimeField(null=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('Created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
