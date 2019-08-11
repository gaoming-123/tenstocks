# encoding: utf-8
# author:  gao-ming
# time:  2019/7/20--9:28
# desc:

from django.urls import path
from .views import LoginView, RegisterView, InfoView, RePasswordView

app_name='user'
urlpatterns = [
    path('login/',LoginView.as_view(),name='登录' ),
    path('register/',RegisterView.as_view(),name='注册' ),
    path('info/',InfoView.as_view(),name='个人资料' ),
    path('register/',RePasswordView.as_view(),name='重置密码' ),
]