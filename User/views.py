from django.shortcuts import render, redirect, reverse
from User.dataoper import *
from Schedule.models import *
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
from django.http import HttpResponse


def index(request):
    unitlist = {'van': {'name': 'van', 'age': '24'}, 'banana': {'name': 'banana', 'age': '9527'},
                'bili': {'name': 'bili', 'age': '123'}, 'leijun': {'name': 'are you ok', 'age': '40'}}
    return render(request, 'User/index.html', {'unitlist': unitlist})


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
        item1 = {'title': 'item1', 'pk': 1}
        item2 = {'title': 'item2', 'pk': 2}
        itemlist = [item1, item2]
        unit1 = {'title': 'unit1', 'itemlist': itemlist}
        unit2 = {'title': 'unit2', 'itemlist': itemlist}
        unitlist = [unit1, unit2]
        unitlist = schedule_list_to_dict(user_sche)
        part_data = add_participate_unit(ScheduleParticipator.objects.filter(participator=request.user))
        if len(part_data['itemlist']) > 0:
            unitlist.append(part_data)
        return render(request, 'User/userprofile.html', {'unitlist': unitlist})
    elif request.method == 'POST':
        oper = request.POST.get('operation')
        pk = request.POST.get('pk')
        if oper == 'Delete':
            if Schedule.objects.get(pk=pk).creator == request.user:
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
            notify_time = datetime.timedelta(request.POST.get('notify_time'))
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            creator = request.user
            type = ScheduleType.objects.create(type_name=request.POST.get('type_name'))
            Schedule.objects.get(pk=pk).update(title=title, description=desc, notify_time=notify_time,
                                               start_time=start_time,
                                               end_time=end_time, creator=creator, type=type)
            return redirect('userprofile', username=request.user.username)


def create_schedule(request, username):
    if request.method == 'GET':
        return render(request, 'User/new_schedule.html')
    else:
        title = request.POST.get('title')
        desc = request.POST.get('description')
        notify_time=datetime.datetime.strftime(request.POST.get('notify_time'),'%H-%M-%S')
        #notify_time = datetime.timedelta(hours=int(notify_time.hour),)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        creator = request.user
        type = ScheduleType.objects.create(type_name=request.POST.get('type_name'))
        Schedule.objects.create(title=title, description=desc, notify_time=request.POST.get('notify_time'), start_time=start_time,
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
            return None
        else:
            datalist = Schedule.objects.filter(title__contains=searchdata)
            unitlist = schedule_list_to_dict(datalist)
            return render(request, 'User/search.html', {'unitlist': unitlist})
    elif request.method == 'POST':
        oper = request.POST.get('operation')
        pk = request.POST.get('pk')
        if oper == 'Add':
            ScheduleParticipator.objects.create(schedule=Schedule.objects.get(pk=pk),
                                                participator=GyroUser.objects.get(username=request.user.username))
            return redirect('userprofile', username=request.user.username)
    return render(request, 'User/search.html')


def schedule_view(request, schedule_pk):
    return render(request, 'User/scheduleprofile.html')


def test(request):
    item1 = {'title': 'item1', 'pk': 1}
    item2 = {'title': 'item2', 'pk': 2}
    itemlist = [item1, item2]
    unit1 = {'title': 'unit1', 'itemlist': itemlist}
    unit2 = {'title': 'unit2', 'itemlist': itemlist}
    unitlist = [unit1, unit2]
    return render(request, 'User/ui.html', {'unitlist': unitlist})
