from django.db import models
from User.models import GyroUser


class ScheduleType(models.Model):
    type_name = models.CharField(max_length=8,
                                 verbose_name="type_name",
                                 help_text="schedule's type name, ")


class Schedule(models.Model):
    title = models.CharField(max_length=32,
                             help_text="schedule's title, less than 32 char.",
                             verbose_name="title")
    description = models.TextField(blank=True,
                                   db_index=True,
                                   verbose_name="description",
                                   help_text="schedule's description.")
    notify_time = models.DurationField(verbose_name="notify_time",
                                       help_text="timedelta to notify user.")
    start_time = models.DateTimeField(verbose_name="start_time",
                                      help_text="schedule's start time.")
    end_time = models.DateTimeField(verbose_name="end_time",
                                    help_text="schedule's end time.")
    creator = models.ForeignKey(GyroUser,
                                on_delete=models.CASCADE,
                                verbose_name="creator",
                                help_text="schedule's creator.")
    participator_count = models.IntegerField(default=1,
                                             verbose_name="participator_count",
                                             help_text="the number of user participate the schedule.")
    type = models.ForeignKey(ScheduleType,
                             on_delete=models.CASCADE,
                             verbose_name="type",
                             help_text="the schedule's type.")

class ScheduleParticipator(models.Model):
    schedule = models.ForeignKey(Schedule,
                                 on_delete=models.CASCADE,
                                 verbose_name="schedule",
                                 help_text="the schedule that user participate.")
    participator = models.ForeignKey(GyroUser,
                                     on_delete=models.CASCADE,
                                     verbose_name="participator",
                                     help_text="the user who participate the schedule.")

