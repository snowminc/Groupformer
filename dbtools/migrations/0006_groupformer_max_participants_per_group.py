# Generated by Django 3.1.7 on 2021-05-06 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbtools', '0005_auto_20210505_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupformer',
            name='max_participants_per_group',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
