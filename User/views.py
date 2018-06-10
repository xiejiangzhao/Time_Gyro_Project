from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'User/index.html')


def userprofile(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    return render(request, 'User/userprofile.html', context={'First_name': first_name, 'Last_name': last_name})
