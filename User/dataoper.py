# coding=utf-8
from django.contrib import auth
from .models import GyroUser
from Schedule.models import *
"""
用户对象包含的内容:
原生的username,email和扩展的schedule_created_count,schedule_attended_count,notice_count,gender,birthday
数据对象包含的内容:
Schedule里面的内容
"""


def authenticate(username: str, password: str):
    """
    :param username:用户名
    :param password: 密码
    :return: 成功返回一个用户对象,不成功返回None
    """
    try:
        u = auth.authenticate(username=username, password=password)
        return u
    except Exception as e:
        return None


def login(request, user):
    """
    :param request:与官方的login保持一致,是一个WSGIRequest
    :param user: 用户对象
    :return: 不必要再去检验密码,登陆后记得修改session,与官方保持一致即可(参考官方的login就可以了)
    """
    auth.login(request, user)


def logout(request):
    auth.logout(request)


def create_user(username: str, password: str, email=None):
    """
    :param username:
    :param password:
    :param email:
    :return: 成功返回一个用户对象,失败返回None,用户名不能同名
    """
    try:
        user = GyroUser.objects.create_user(username, email, password)
        return user
    except Exception as e:
        return None


def change_user(username, password, gender, birthday):
    """
    :param username:
    :param password:
    :param gender:
    :param birthday:
    :return: 根据以上信息修改,成功返回True,失败返回Faslse,传入参数都是字符串
    """
    try:
        user = GyroUser.objects.get(username=username)
        user.set_password(password)
        user.gender = gender
        user.birthday = birthday
        user.save()
        return True
    except Exception as e:
        return False


def user_exist(username):
    user = GyroUser.objects.get(username=username)
    if len(user) != 0:
        return True
    else:
        return False

def create_Schedule(title,desc,notify_time,start_time,end_time,creator,participator_count,type,user):
    """
    一个用户创建一个任务,最后一个你在注释里说明要用户对象还是用户名
    :param title:
    :param desc:
    :param notify_time:
    :param start_time:
    :param end_time:
    :param creator:
    :param participator_count:
    :param type:
    :param user:
    :return:
    """
    pass

def delete_Schedule(title,desc,notify_time,start_time,end_time,creator,participator_count,type,user):
    """
    用户创始人删除任务,最后一个你在注释里说明要用户对象还是用户名
    :param title:
    :param desc:
    :param notify_time:
    :param start_time:
    :param end_time:
    :param creator:
    :param participator_count:
    :param type:
    :param user:
    :return:
    """
    pass
def change_Schedule(title,desc,notify_time,start_time,end_time,creator,participator_count,type,user):
    """
    用户创始人修改任务,最后一个你在注释里说明要用户对象还是用户名
    :param title:
    :param desc:
    :param notify_time:
    :param start_time:
    :param end_time:
    :param creator:
    :param participator_count:
    :param type:
    :param user:
    :return:
    """
def attend_Sechedule(title,desc,notify_time,start_time,end_time,creator,participator_count,type,user):
    """
    用户参与任务
    :param title:
    :param desc:
    :param notify_time:
    :param start_time:
    :param end_time:
    :param creator:
    :param participator_count:
    :param type:
    :param user:
    :return:
    """