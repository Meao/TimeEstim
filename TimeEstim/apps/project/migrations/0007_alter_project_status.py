# Generated by Django 3.2 on 2021-04-16 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_step_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Активный'), ('archived', 'В архиве')], default='ongoing', max_length=20),
        ),
    ]
