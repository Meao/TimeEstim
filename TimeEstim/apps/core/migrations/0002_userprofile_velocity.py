# Generated by Django 3.2 on 2021-04-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='velocity',
            field=models.IntegerField(default=0),
        ),
    ]
