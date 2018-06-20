from django.shortcuts import render, redirect, reverse
from User.dataoper import *
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse

@login_required
def index(request):
    print(request.user.is_aunthenticated)
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
        return render(request, 'User/login.html', context)


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

def userprofile(request, username):
    return render(request, 'User/userprofile.html')


def test(request):
    return render(request, 'User/register.html')
