# Generated by Django 2.0.4 on 2018-06-11 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20180610_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='XeroContactID',
            field=models.CharField(db_index=True, default='', max_length=64, null=True),
        ),
    ]