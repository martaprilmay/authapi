# Generated by Django 3.1.6 on 2021-02-11 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210211_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='password',
            field=models.CharField(max_length=64),
        ),
    ]
