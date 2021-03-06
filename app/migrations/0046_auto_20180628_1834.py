# Generated by Django 2.0.4 on 2018-06-28 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20180628_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeroalljournals',
            name='CategoryName',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xeroalljournals',
            name='OptionName',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xeroalljournals',
            name='Status',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='xeroalljournals',
            name='TrackingCategoryID',
            field=models.CharField(blank=True, default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='xeroalljournals',
            name='TrackingOptionID',
            field=models.CharField(blank=True, default='', max_length=64, null=True),
        ),
    ]
