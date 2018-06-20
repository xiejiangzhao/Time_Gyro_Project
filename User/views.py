from django.shortcuts import render, redirect, reverse
from User.dataoper import *
from Schedule.models import *
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
from django.http import HttpResponse



def index(request):
    #print(request.user.is_aunthenticated)
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
        res =  create_user(username, password, email)
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
        user_sche=Schedule.objects.filter(creator=request.user)[0]

        user_data = Schedule.objects.filter(creator=request.user)
        dur=datetime.timedelta(days=1,hours=2)
        ScheduleType.objects.create(type_name='xietest')
        thistype=ScheduleType.objects.filter(type_name='xietest')
        Schedule.objects.create(title='aaa',notify_time=dur,start_time='2017-06-18',end_time='2017-06-18',creator=request.user,type=thistype[0])
        print(user_data[0].pk)
        context = {'aaa': ['d1', 'd2']}
        return render(request, 'User/userprofile.html', context)

def test(request):
    return render(request, 'User/register.html')
