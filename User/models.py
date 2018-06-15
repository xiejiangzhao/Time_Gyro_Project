from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,AbstractUser,User
# Create your models here.
from django.db import models


class GyroUser(AbstractUser):
    # models.OneToOneField(User,on_delete=models.CASCADE)
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
    gender = models.BooleanField(default=True,
                                 verbose_name="gender",
                                 help_text="user's gender, True is Male, False is Female, default is True.")
    birthday = models.DateField(null=True, verbose_name="birthday",
                                help_text="user's birthday, must be YYYY-MM-DD")

