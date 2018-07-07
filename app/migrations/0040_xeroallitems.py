# Generated by Django 2.0.4 on 2018-06-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_xeroallcurrencies'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemID', models.CharField(blank=True, default='', max_length=64, unique=True)),
                ('Code', models.CharField(blank=True, default='', max_length=50, unique=True)),
                ('Name', models.CharField(blank=True, default='', max_length=100)),
                ('IsSold', models.BooleanField(default=False)),
                ('IsPurchased', models.BooleanField(default=False)),
                ('Description', models.CharField(blank=True, default='', max_length=1000)),
                ('PurchaseDescription', models.CharField(blank=True, default='', max_length=1000)),
                ('IsTrackedAsInventory', models.BooleanField(default=False)),
                ('InventoryAssetAccountCode', models.CharField(blank=True, default='', max_length=50)),
                ('TotalCostPool', models.FloatField(default=0, null=True)),
                ('QuantityOnHand', models.FloatField(default=0, null=True)),
                ('UpdatedDateUTC', models.DateTimeField(null=True)),
                ('COGSAccountCode', models.CharField(blank=True, default='', max_length=50)),
                ('UnitPrice', models.FloatField(default=0, null=True)),
                ('AccountCode', models.CharField(blank=True, default='', max_length=50)),
                ('TaxType', models.CharField(blank=True, default='', max_length=20)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('Created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
