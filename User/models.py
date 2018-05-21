from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nick_name = models.CharField(max_length=32,
                                 blank=True,
                                 verbose_name="nick_name",
                                 help_text="user's nick name, can be not fill in form.")
    date_last_logged_in = models.DateTimeField(null=True,
                                               verbose_name="date_last_logged_in",
                                               help_text="user's last login time, use timezone.now() to fill it.")
    schedule_created_count = models.IntegerField(default=0,
                                                 verbose_name="schedule_created_count",
                                                 help_text="the number of schedule that user created, can only be "
                                                           "modified by business layer, NOT use store procedure!")
    schedule_attended_count = models.IntegerField(default=0,
                                                  verbose_name="schedule_attended_count",
                                                  help_text="the number of schedule that user attended, exclude user "
                                                            "created, can only be modified by business layer, "
                                                            "NOT use store procedure!")
    notice_count = models.IntegerField(default=0,
                                       verbose_name="notice_count",
                                       help_text="the number of notice that user created, can only be modified by "
                                                 "business layer, NOT use store procedure!")

    class Meta(AbstractUser.Meta):
        pass
