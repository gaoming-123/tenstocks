# encoding: utf-8
# author:  gao-ming
# time:  2019/7/21--21:00
# desc:

from django.urls import path
from .views import *


app_name='stocks'
urlpatterns = [
    # path('login/',LoginView.as_view(),name='登录' ),
    path('index/',Stocks.as_view(),name='首页' ),
    path('fivedata/',Add_first_data.as_view(),name='添加五日资金数据' ),
    path('allstocks/',New_stocks.as_view(),name='更新a股个股' ),
    # path('^$',Stocks.as_view(),name='首页' ),

]