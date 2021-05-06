# Generated by Django 3.1.7 on 2021-05-05 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbtools', '0004_merge_20210420_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupformer',
            name='associated_user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attribute_selection',
            name='value',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='project_selection',
            name='value',
            field=models.IntegerField(),
        ),
    ]