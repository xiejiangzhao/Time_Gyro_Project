# Generated by Django 2.0.4 on 2018-06-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="schedule's title, less than 32 char.", max_length=32, verbose_name='title')),
                ('description', models.TextField(blank=True, db_index=True, help_text="schedule's description.", verbose_name='description')),
                ('notify_time', models.DurationField(help_text='timedelta to notify user.', verbose_name='notify_time')),
                ('start_time', models.DateTimeField(help_text="schedule's start time.", verbose_name='start_time')),
                ('end_time', models.DateTimeField(help_text="schedule's end time.", verbose_name='end_time')),
                ('participator_count', models.IntegerField(default=1, help_text='the number of user participate the schedule.', verbose_name='participator_count')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleParticipator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(help_text="schedule's type name, ", max_length=8, verbose_name='type_name')),
            ],
        ),
    ]