# Generated by Django 4.1 on 2022-08-21 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catcher', '0002_logmodel_origin_alter_logmodel_operation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmodel',
            name='origin',
            field=models.CharField(max_length=30),
        ),
    ]