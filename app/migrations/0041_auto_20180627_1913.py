# Generated by Django 2.0.4 on 2018-06-27 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_xeroallitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xeroallitems',
            old_name='AccountCode',
            new_name='CostAccountCode',
        ),
        migrations.RenameField(
            model_name='xeroallitems',
            old_name='TaxType',
            new_name='CostTaxType',
        ),
        migrations.AddField(
            model_name='xeroallitems',
            name='SalesAccountCode',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='xeroallitems',
            name='SalesTaxType',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='xeroallitems',
            name='SalesUnitPrice',
            field=models.FloatField(default=0, null=True),
        ),
    ]
