from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import GyroUser
from django.contrib.auth.models import User

admin.site.register(User,GyroUser)