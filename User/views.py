from django.shortcuts import render, redirect, reverse
from User.dataoper import *
from Schedule.models import *
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
from django.http import HttpResponse


def index(request):
    # print(request.user.is_aunthenticated)
    return render(request, 'User/index.html')


def login_view(request):
    context = {'Logstatus': 'False'}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userprofile', username=username)
        return render(request, 'User/login.html', context)
    else:
        context['Logstatus'] = 'Init'
        return render(request, 'User/login.html')


def register(request):
    context = {'Regstatus': 'False'}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        res = create_user(username, password, email)
        if res is not None:
            return redirect('userprofile', username=username)
        else:
            return render(request, 'User/register.html', context)
    else:
        context['Regstatus'] = 'Init'
        return render(request, 'User/register.html', context)


@login_required
def userprofile(request, username):
    print(request.user.is_authenticated)
    if request.method == 'GET':
        user_sche = Schedule.objects.filter(creator=request.user)
        context = schetodict(user_sche)
        context['username'] = request.user.username
        return render(request, 'User/userprofile.html', context)


def scheduleprofile(request, schedulepk):
    if request.method == 'GET':
        obj_sche=Schedule.objects.get(pk=schedulepk)
        context={'title':obj_sche.title,'desc':obj_sche.description,}
    pass


def create_schedule(request, username):
    if request.method == 'GET':
        return render(request, 'User/new_schedule.html')
    else:
        title = request.POST.get('title')
        desc = request.POST.get('description')
        notify_time = datetime.timedelta(days=int(request.POST.get('days')), hours=int(request.POST.get('hours')))
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        creator = request.user
        type = ScheduleType.objects.create(type_name=request.POST.get('type_name'))
        Schedule.objects.create(title=title, description=desc, notify_time=notify_time, start_time=start_time,
                                end_time=end_time, creator=creator, type=type)
        return redirect('userprofile', username=username)


def test(request):
    return render(request, 'User/register.html')
