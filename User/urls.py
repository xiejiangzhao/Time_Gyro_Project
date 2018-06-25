from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('test/', views.test, name='test'),
    path('register/', views.register, name='register'),
    path('<str:username>/', views.userprofile, name='userprofile'),
    path('<str:username>/create_schedule/', views.create_schedule, name='create_schedule')
]
