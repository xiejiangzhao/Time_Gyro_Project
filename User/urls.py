from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('<str:username>/',views.userprofile,name='user_profile')
]