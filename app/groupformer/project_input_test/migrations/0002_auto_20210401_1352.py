# Generated by Django 3.1.7 on 2021-04-01 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_input_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_homogenous', models.BooleanField()),
                ('is_continuous', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='attribute_selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='GroupFormer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_name', models.CharField(max_length=200)),
                ('prof_email', models.CharField(max_length=200)),
                ('class_section', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_email', models.CharField(max_length=200)),
                ('part_name', models.CharField(max_length=200)),
                ('attributes', models.ManyToManyField(through='project_input_test.attribute_selection', to='project_input_test.Attribute')),
                ('desired_partner', models.ManyToManyField(related_name='_participant_desired_partner_+', to='project_input_test.Participant')),
                ('gf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.groupformer')),
            ],
        ),
        migrations.CreateModel(
            name='project_selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.participant')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.project')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='projects',
            field=models.ManyToManyField(through='project_input_test.project_selection', to='project_input_test.Project'),
        ),
        migrations.AddField(
            model_name='attribute_selection',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.participant'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='gf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_input_test.groupformer'),
        ),
        migrations.AddField(
            model_name='project',
            name='gf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project_input_test.groupformer'),
            preserve_default=False,
        ),
    ]
