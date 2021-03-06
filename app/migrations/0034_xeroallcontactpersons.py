# Generated by Django 2.0.4 on 2018-06-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20180626_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAllContactPersons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactID', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('FirstName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('LastName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('EmailAddress', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('IncludeInEmails', models.BooleanField(default=False)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('Created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
