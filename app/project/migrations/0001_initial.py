# Generated by Django 4.0 on 2021-12-31 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=250)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('state', models.BooleanField(default=False, verbose_name='Is it done')),
                ('is_next_action', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('done', models.DateTimeField(blank=True, null=True)),
                ('done_when', models.CharField(max_length=250)),
                ('state', models.CharField(choices=[('AC', 'Active'), ('DO', 'Done'), ('DE', 'Deleted'), ('SO', 'Someday/Maybe')], default='AC', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateTimeField()),
                ('week_end', models.DateTimeField()),
                ('actions', models.ManyToManyField(to='project.Action')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]