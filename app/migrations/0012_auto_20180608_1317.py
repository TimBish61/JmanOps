# Generated by Django 2.0.4 on 2018-06-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180608_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeroalloverpayments',
            name='Type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='xeroallprepayments',
            name='Type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
