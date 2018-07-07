# Generated by Django 2.0.4 on 2018-06-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_xeroinvoices'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroCreditNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('ContactNumber', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Date', models.DateTimeField(auto_now=True)),
                ('Status', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('LineAmountTypes', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('SubTotal', models.FloatField(default=0)),
                ('TotalTax', models.FloatField(default=0)),
                ('Total', models.FloatField(default=0)),
                ('UpdatedDateUTC', models.DateTimeField(auto_now=True)),
                ('CurrencyCode', models.CharField(blank=True, default='', max_length=4, null=True)),
                ('CurrencyRate', models.FloatField(default=1, null=True)),
                ('Type', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('Reference', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('RemainingCredit', models.FloatField(default=0)),
                ('HasAttachments', models.BooleanField(default=False)),
                ('CreditNoteID', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('CreditNoteNumber', models.CharField(blank=True, default='', max_length=50, null=True)),
            ],
        ),
    ]
