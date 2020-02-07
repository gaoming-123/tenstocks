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
    path('monitor/',Monitor.as_view(),name='监控' ),
    path('fivedata/',Add_first_data.as_view(),name='添加五日资金数据' ),
    path('allstocks/',New_stocks.as_view(),name='更新a股个股' ),
    path('fiveday/',Five_day_data.as_view(),name='更新五日资金数据' ),
    path('rzrq/<code>/',Stock_dfcf_RzRq.as_view(),name='获取东方财富融资融券数据' ),
    path('financeq/<code>/',Finance_quota.as_view(),name='获取财务指标数据' ),
    path('rzrqall/',Stock_tushare_RzRq.as_view(),name='获取tushare全部融资融券数据' ),
    path('detail/<code>/',StockDetail.as_view(),name='个股详情页' ),
    path('tradedata/<code>/',StockTradeData.as_view(),name='个股daily数据' ),
    path('pick/',PickStock.as_view(),name='筛选股票' ),
    path('pickstock/<code>/',TradeStock.as_view(),name='筛选股票' ),
    path('test/',Test.as_view(),name='测试' ),
    path('fquota/<code>/',GetFinanceQuota.as_view(),name='财务指标数据' ),
    path('mdq/',CalcuMarketDayQuota.as_view(),name='全市场每日指标' ),

    # path('^$',Stocks.as_view(),name='首页' ),

]