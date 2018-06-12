from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.utils import timezone
from .models import User
from learning_logs.forms import UserCreationForm, UserForm
# Create your views here.
def userlogin(request):
    if request.method != 'POST':
        form = UserForm()
        
    else:
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # update the last logged date
            user.date_last_logged_in = timezone.now()
            user.save()
            # login
            login(request, user)
            # redirect to the first page of schedule list
            return HttpResponseRedirect(reverse('schedule:schedule_list'), args=[1])
    
    return render(request,'user/login.html',{'form':form})

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.date_last_logged_in = timezone.now()
            new_user.save()
            form.save_m2m() 
            # 自动登录并重定向到主页
            authenticated_user = authenticate(username=new_user.username,
                    password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('schedule:schedule_list'), args=[1])

    context = {'form': form}
    return render(request, 'user/register.html', context)


def logout_view(request):
    """user log out"""
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))



