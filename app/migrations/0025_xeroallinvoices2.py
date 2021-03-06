# Generated by Django 2.0.4 on 2018-06-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20180611_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllInvoices2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('ContactID', models.CharField(blank=True, default='', max_length=64)),
                ('ContactNumber', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Date', models.DateTimeField(null=True)),
                ('DueDate', models.DateTimeField(null=True)),
                ('Status', models.CharField(max_length=20, null=True)),
                ('LineAmountTypes', models.CharField(max_length=20, null=True)),
                ('SubTotal', models.FloatField(default=0, null=True)),
                ('TotalTax', models.FloatField(default=0, null=True)),
                ('Total', models.FloatField(default=0, null=True)),
                ('TotalDiscount', models.FloatField(default=0, null=True)),
                ('UpdatedDateUTC', models.DateTimeField(null=True)),
                ('CurrencyCode', models.CharField(blank=True, max_length=4, null=True)),
                ('CurrencyRate', models.FloatField(default=1, null=True)),
                ('InvoiceID', models.CharField(default='', max_length=64)),
                ('InvoiceNumber', models.CharField(default='', max_length=50)),
                ('Reference', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('BrandingThemeID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('Url', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('SentToContact', models.BooleanField(default=False)),
                ('ExpectedPaymentDate', models.DateTimeField(null=True)),
                ('PlannedPaymentDate', models.DateTimeField(null=True)),
                ('HasAttachments', models.BooleanField(default=False)),
                ('AmountDue', models.FloatField(default=0, null=True)),
                ('AmountPaid', models.FloatField(default=0, null=True)),
                ('CISDeduction', models.FloatField(default=0, null=True)),
                ('FullyPaidOnDate', models.DateTimeField(null=True)),
                ('AmountCredited', models.FloatField(default=0, null=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('Created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
