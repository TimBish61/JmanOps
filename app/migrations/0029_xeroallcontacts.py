# Generated by Django 2.0.4 on 2018-06-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_xeroallcreditnotes_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactID', models.CharField(blank=True, default='', max_length=64)),
                ('ContactNumber', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('AccountNumber', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('ContactStatus', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('FirstName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('LastName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('EmailAddress', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('SkypeUserName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('BankAccountDetails', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('TaxNumber', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('AccountsReceivableTaxType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('AccountsPayableTaxType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('AddressType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('AddressLine1', models.CharField(blank=True, default='', max_length=160, null=True)),
                ('AddressLine2', models.CharField(blank=True, default='', max_length=160, null=True)),
                ('AddressLine3', models.CharField(blank=True, default='', max_length=160, null=True)),
                ('AddressLine4', models.CharField(blank=True, default='', max_length=160, null=True)),
                ('City', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Region', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('PostalCode', models.CharField(blank=True, default='', max_length=12, null=True)),
                ('Country', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('AttentionTo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('IsSupplier', models.BooleanField(default=False)),
                ('IsCustomer', models.BooleanField(default=False)),
                ('DefaultCurrency', models.CharField(blank=True, default='', max_length=4, null=True)),
                ('UpdatedDateUTC', models.DateTimeField(null=True)),
            ],
        ),
    ]
