from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_out, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('schedule/<str:schedule_pk>', views.schedule_view, name='schedule'),
    path('<str:username>/', views.userprofile, name='userprofile'),
    path('<str:username>/create_schedule/', views.create_schedule, name='create_schedule'),
    path('<str:username>/setting/', views.setting, name='setting')
]
