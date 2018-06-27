from django.shortcuts import render, redirect, reverse
from User.dataoper import *
from Schedule.models import *
from django.contrib.auth.decorators import login_required
import datetime
import schedule
import time
import threading
# Create your views here.
from django.http import HttpResponse

import itchat
from itchat.content import TEXT
from itchat import send
import json


def index(request):
    return render(request, 'User/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next', '') == '':
                return redirect('userprofile', username=username)
            else:
                return redirect(request.GET.get('next', ''))
        return render(request, 'User/login.html', {'Logstatus': 'False'})
    else:
        return render(request, 'User/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        res = create_user(username, password, email)
        if res is not None:
            return redirect('userprofile', username=username)
        else:
            return render(request, 'User/register.html', {'Regstatus': 'False'})
    else:
        return render(request, 'User/register.html')


@login_required
def userprofile(request, username):
    if username != request.user.username:
        return redirect('userprofile', username=request.user.username)
    if request.method == 'GET':
        user_sche = Schedule.objects.filter(creator=request.user)
        unitlist = schedule_list_to_dict(user_sche)
        part_data = add_participate_unit(ScheduleParticipator.objects.filter(participator=request.user))
        if len(part_data['itemlist']) > 0:
            unitlist.append(part_data)
        return render(request, 'User/userprofile.html', {'unitlist': unitlist, 'username': request.user.username})
    elif request.method == 'POST':
        oper = request.POST.get('operation')
        pk = request.POST.get('pk')
        if oper == 'Delete':
            if Schedule.objects.get(pk=pk).creator == request.user:
                part_list = ScheduleParticipator.objects.filter(schedule=Schedule.objects.get(pk=pk))
                for i in part_list:
                    i.delete()
                Schedule.objects.get(pk=pk).delete()
            else:
                ScheduleParticipator.objects.get(participator=GyroUser.objects.get(username=request.user.username),
                                                 schedule=Schedule.objects.get(pk=pk)).delete()
            return redirect('userprofile', username=request.user.username)


def scheduleprofile(request, schedulepk):
    if request.method == 'GET':
        obj_sche = Schedule.objects.get(pk=schedulepk)
        context = {'title': obj_sche.title, 'desc': obj_sche.description, 'notify_time_day': obj_sche.notify_time.days,
                   'start_time': obj_sche.start_time,
                   'end_time': obj_sche.end_time, 'participator_count': obj_sche.participator_count,
                   'type': obj_sche.type}
        return render(request, 'User/new_schedule.html', context)
    elif request.method == 'POST':
        oper = request.POST.get('operation')
        pk = request.POST.get('pk')
        if oper == 'Delete':
            Schedule.objects.get(pk=pk).delete()
            return redirect('userprofile', username=request.user.username)
        elif oper == 'Update':
            title = request.POST.get('title')
            desc = request.POST.get('description')
            notify_time = datetime.timedelta(days=int(request.POST.get('notify_day')),hours=int(request.POST.get('notify_hour')))
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            creator = request.user
            type = ScheduleType.objects.get_or_create(type_name=request.POST.get('type_name'))
            sche=Schedule.objects.get(pk=pk)
            sche.title=title
            sche.description = desc
            sche.title = title
            sche.notify_time=notify_time
            sche.start_time=start_time
            sche.end_time=end_time
            sche.type=type
            sche.save()
            return redirect('userprofile', username=request.user.username)


def create_schedule(request, username):
    if request.method == 'GET':
        return render(request, 'User/new_schedule.html')
    else:
        title = request.POST.get('title')
        desc = request.POST.get('description')
        notify_time = datetime.timedelta(days=int(request.POST.get('notify_day')),
                                         hours=int(request.POST.get('notify_hour')))
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        creator = request.user
        type = ScheduleType.objects.create(type_name=request.POST.get('type_name'))
        Schedule.objects.create(title=title, description=desc, notify_time=notify_time,
                                start_time=start_time,
                                end_time=end_time, creator=creator, type=type)
        return redirect('userprofile', username=username)


@login_required
def login_out(request):
    logout(request)
    return redirect('index')


def setting(request, username):
    if request.method == 'GET':
        context = {'username': request.user.username, 'gender': 'Male' if request.user.gender is True else 'Female',
                   'birthday': request.user.birthday}
        return render(request, 'User/setting.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        userobj = GyroUser.objects.get(username=request.user.username)
        if password != '':
            userobj.set_password(password)
        userobj.gender = gender
        userobj.birthday = birthday
        userobj.save()
        context = {'username': request.user.username, 'gender': 'Male' if gender is True else 'Female',
                   'birthday': birthday}
        return render(request, 'User/setting.html', context)


@login_required
def search(request):
    if request.method == 'GET':
        searchdata = request.GET.get('q', '')
        if searchdata == '':
            datalist = Schedule.objects.all()
            unitlist = schedule_list_to_dict(datalist)
            return render(request, 'User/search.html', {'unitlist': unitlist, 'username': request.user.username})
        else:
            datalist = Schedule.objects.filter(title__contains=searchdata)
            unitlist = schedule_list_to_dict(datalist)
            return render(request, 'User/search.html', {'unitlist': unitlist, 'username': request.user.username})
    elif request.method == 'POST':
        oper = request.POST.get('operation')
        pk = request.POST.get('pk')
        if oper == 'Add':
            ScheduleParticipator.objects.create(schedule=Schedule.objects.get(pk=pk),
                                                participator=GyroUser.objects.get(username=request.user.username))
            return redirect('userprofile', username=request.user.username)
    return render(request, 'User/search.html')


def schedule_view(request, schedule_pk):
    print(schedule_pk)
    sche_obj = Schedule.objects.get(pk=schedule_pk)
    if request.method == 'GET':
        title = sche_obj.title
        desc = sche_obj.description
        notify_day = sche_obj.notify_time.days
        start_time = sche_obj.start_time
        end_time = sche_obj.end_time
        creator = request.user.username
        type = sche_obj.type.type_name
        context = {'title': title, 'desc': desc, 'notify_day': notify_day,
                   'start_time': start_time, 'end_time': end_time, 'creator': creator, 'type': type}
        return render(request, 'User/scheduleprofile.html', context)
    else:
        oper = request.POST.get('operation')
        if oper == 'Delete':
            tmp = ScheduleParticipator.objects.filter(schedule=Schedule.objects.get(pk=schedule_pk))
            for i in tmp:
                i.delete()
            Schedule.objects.get(pk=schedule_pk).delete()
            return redirect('userprofile', username=request.user.username)
        elif oper == 'Update':
            title = request.POST.get('title')
            desc = request.POST.get('description')
            notify_time = datetime.timedelta(days=int(request.POST.get('notify_day')),
                                             hours=int(request.POST.get('notify_hour')))
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            creator = request.user
            type = ScheduleType.objects.create(type_name=request.POST.get('type_name'))
            sche = Schedule.objects.get(pk=schedule_pk)
            sche.title = title
            sche.description = desc
            sche.title = title
            sche.notify_time = notify_time
            sche.start_time = start_time
            sche.end_time = end_time
            sche.type = type
            sche.save()
            return redirect('userprofile', username=request.user.username)


def wechat_module():
    itchat_user_dict = {}
    itchat_user_dict_reverse = {}
    itchat.auto_login(hotReload=False)
    client = itchat.search_friends(nickName='一个亿')[0]['UserName']
    a = itchat.search_friends(nickName='一个亿')

    @itchat.msg_register(TEXT)
    def text_reply(msg):
        print(msg['FromUserName'])
        if msg['FromUserName'] == client:
            msgdata = json.loads(msg['Text'])
            res = {}
            if msgdata['MessageType'] == 1:
                res['MessageType'] = 1
                res['ToUserName'] = msgdata['FromUserName']
                if authenticate(msgdata['User'], msgdata['Password']):
                    res['AuthenticationResult'] = True
                    itchat_user_dict[msgdata['FromUserName']] = msgdata['User']
                    itchat_user_dict_reverse[msgdata['User']] = msgdata['FromUserName']
                else:
                    res['AuthenticationResult'] = False
                print("Msg to client")
                print(res)
                send(json.dumps(res), client)
                print(itchat_user_dict)
            elif msgdata['MessageType'] == 2:
                res['MessageType'] = 2
                res['Message'] = ""
                res['ToUserName'] = msgdata['FromUserName']
                username = itchat_user_dict[msgdata['FromUserName']]
                user_sche = Schedule.objects.filter(creator=GyroUser.objects.get(username=username))
                unitlist = schedule_list_to_dict(user_sche)
                part_data = add_participate_unit(
                    ScheduleParticipator.objects.filter(participator=GyroUser.objects.get(username=username)))
                if len(part_data['itemlist']) > 0:
                    unitlist.append(part_data)
                for unit in unitlist:
                    res['Message'] += unit['title'] + ':'
                    for item in unit['itemlist']:
                        res['Message'] += item['title'] + ','
                print("Msg to client")
                print(res)
                send(json.dumps(res), msg['FromUserName'])

    def job():
        while True:
            print("Gyro Wechat server is working")
            date_now = datetime.datetime.now().timestamp()
            sche_all = Schedule.objects.all()
            for sche in sche_all:
                if date_now >= (sche.end_time - sche.notify_time).timestamp():
                    print('Delete', sche.title, sche.pk)
                    res = {'MessageType': 2}
                    try:
                        res['ToUserName'] = itchat_user_dict_reverse[sche.creator.username]
                    except:
                        tmp = ScheduleParticipator.objects.filter(schedule=sche)
                        for i in tmp:
                            i.delete()
                        sche.delete()
                        continue
                    res['Message'] = '任务提醒:' + sche.title
                    print("Msg to client")
                    print(res)
                    send(json.dumps(res), client)
                    tmp = ScheduleParticipator.objects.filter(schedule=sche)
                    for i in tmp:
                        i.delete()
                    sche.delete()
            time.sleep(10)

    def mytime():
        itchat.run()

    t = threading.Thread(target=job, name='it')
    v = threading.Thread(target=mytime, name='it1')
    v.start()
    t.start()

#wechat_module()