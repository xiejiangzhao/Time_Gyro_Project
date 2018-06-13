from django.shortcuts import render
from User.models import *
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'User/index.html')


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    context = {'Logstatus': False}
    request.session['Logstatus'] = False
    user_data = User.objects.filter(username=username,password=password)
    if len(user_data) != 0:
        context['Logstatus']=True
        request.session['Logstatus']=True
    print(request.session['Logstatus'])
    return render(request, 'User/login.html', context)


def userprofile(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    b = User()
    return render(request, 'User/userprofile.html', context={'First_name': first_name, 'Last_name': last_name})


def test(request, d):
    return render(request, 'User/index.html')
