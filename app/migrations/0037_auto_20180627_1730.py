# Generated by Django 2.0.4 on 2018-06-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_xeroallaccounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeroallaccounts',
            name='Description',
            field=models.CharField(blank=True, default='', max_length=240),
        ),
    ]
