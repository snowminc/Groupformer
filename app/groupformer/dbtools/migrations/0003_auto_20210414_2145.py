# Generated by Django 3.1.7 on 2021-04-15 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbtools', '0002_auto_20210412_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=240),
        ),
    ]
