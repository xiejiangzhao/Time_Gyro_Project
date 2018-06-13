from django.conf.urls import url

from . import views

app_name = 'User'

urlpatterns = [
    # 登录页面
    url(r'^login/$', views.userlogin, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name="register"),
]