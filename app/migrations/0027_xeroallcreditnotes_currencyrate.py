# Generated by Django 2.0.4 on 2018-06-25 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_delete_xeroallinvoices2'),
    ]

    operations = [
        migrations.AddField(
            model_name='xeroallcreditnotes',
            name='CurrencyRate',
            field=models.FloatField(default=1, null=True),
        ),
    ]
