# Generated by Django 2.0.4 on 2018-06-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_xeroalloverpayments_xeroallprepayments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeroalloverpayments',
            name='Name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
