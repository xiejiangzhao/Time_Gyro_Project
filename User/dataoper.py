# coding=utf-8
from django.contrib import auth
from .models import GyroUser

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


def create_user(username:str,password:str,email=None):
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

def change_user(username,password,gender,birthday):
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