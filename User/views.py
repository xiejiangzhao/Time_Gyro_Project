from django.shortcuts import render, redirect, reverse
from User.dataoper import *
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'User/index.html')


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    context = {'Logstatus': 'False'}
    if username == None: context['Logstatus'] = 'Init'
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('userprofile', username=username)
    return render(request, 'User/login.html', context)

def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    context = {'Regstatus': 'False'}
    if username == None:
        context['Regstatus'] = 'Init'
        return render(request, 'User/register.html', context)
    else:
        res = create_user(username, password, email)
        if res is not None:
            return redirect('userprofile', username=username)
        else:
            return render(request, 'User/register.html', context)


def userprofile(request, username):
    return render(request, 'User/userprofile.html')


def test(request):
    return render(request, 'User/register.html')
