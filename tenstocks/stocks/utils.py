# desc: 工具类函数

import datetime
import hashlib
import json
import re
import time
import requests
from tenstocks.settings import BASE_DIR
from .models import A_stocks,  DB_N, TuShareRzRq, FinanceQuota, MarketDayQuota, TradeData, RzRq
import numpy
import pandas as pd
import tushare as ts

MY_TOKEN = '4516ff6d7ad8bd6c3393fc750c46fb2eed9f0ee3996ecc8f656943a1'


def get_md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def check_stock_exist(code):
    try:
        stock = A_stocks.objects.filter(symbol=code)[0]
    except:
        return None
    return stock


# 更新A股的股票
def get_all_stocks():
    """获取A股市场全部个股 代码 编号等"""
    pro = ts.pro_api('4516ff6d7ad8bd6c3393fc750c46fb2eed9f0ee3996ecc8f656943a1')
    stocks_list = pro.stock_basic(exchange='', list_status='L',
                                  fields='ts_code,symbol,name,area,industry,fullname,enname,'
                                         'market,exchange,curr_type,list_status,list_date,is_hs')  # ,delist_date 该字段未要
    print(stocks_list.shape)
    #  将自增设置为1
    #  alter table tenstocks.stocks_a_stocks  AUTO_INCREMENT = 1
    for i in range(stocks_list.shape[0]):
        try:
            stock = stocks_list.iloc[i, :]
            A_stocks.objects.create(**dict(stock))
        except Exception as e:
            print(e)


# 添加历史数据
def add_xlsx_data(xlsx_file_name,model_class):
    """从xlsx文件 添加历史数据"""
    org_data = pd.read_excel(f'{BASE_DIR}/{xlsx_file_name}', encoding='utf-8')
    org_data = org_data.fillna(0)
    for i in range(org_data.shape[0]):
        row = org_data.iloc[i, :]
        row = dict(row)
        model_class.objects.create(**row)



# 获取五日行业资金流
def get_five_day_data():
    """获取五日行业资金流 及 行业净流入第一的公司 数据 """
    # 请求头
    header = {
        'Referer': 'http://data.eastmoney.com/bkzj/hy.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    }
    # 5日行业资金流第一页url   两者token一样,需要到第一次请求网页中提取
    url_5 = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?" \
            "cmd=C._BKHY&type=ct&st=(BalFlowMainNet5)&sr=-1&p=1&ps=61&" \
            "js=var%20kOJqxAcC={pages:(pc),data:[(x)]}&" \
            "token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK5&rt=51556320"
    response = requests.get(url_5, headers=header)
    response.encoding = "utf-8"
    # 取出61个字符串
    datas = re.findall('"(.*?)"', response.text)
    if len(datas) != 61:
        return '错误'

    money_dict = {}
    company_dict = {}
    for data in datas:
        # 把每个字符串拆分成列表
        a = data.split(",")
        try:
            key = DB_N.get(a[2])
            money_dict[key] = (int(a[4]) / 10000)
            company_dict[key] = a[14]
        except:
            continue
    # list = []
    # for data in datas:
    #     # 把每个字符串拆分成列表
    #     list.append(data.split(","))
    # # 提取行业以及金额
    # # new_data = []
    # for a in list:
    #     # print(len(a))
    #     try:
    #         # 将行业,资金流,公司组成列表
    #         # new_data.append([a[2], (int(a[4]) / 10000), a[14]])
    #         key = DB_N.get(a[2])
    #         money_dict[key] = (int(a[4]) / 10000)
    #         # print(type(d[1]))
    #         company_dict[key] = a[14]
    #     except:
    #         continue

    return money_dict, company_dict


# 从东方财富网获取个股融资融券数据
def get_rongzirongquan_from_dfcf(stock, all=False):
    """从东方财富网获取个股融资融券数据 并解析"""
    # data = {
    #     "date": '日期',
    #     "scode": "601166",  # code
    #     "spj": '收盘价',  #
    #     "market": "融资融券_沪证",
    #     "secname": "兴业银行",  # 名称
    #     "zdf": '涨跌幅%',  #
    #
    #     "rzmre": '融资买入额(亿)',
    #     "rzche": '融资偿还额(亿)',
    #     "rzjme": '融资净买入(亿)',
    #     "rzye": '融资余额(亿)',
    #
    #     "rqmcl": '融券卖出量(股)',
    #     "rqchl": '融券偿还量(股)',
    #     "rqjmg": '融券净卖(股)',
    #     "rqyl": '融券余量(股)',
    #     "rqye": '融券余额(元)',
    #
    #     "rzrqye": '融资融券余额(亿)',
    #     "rzyezb": '余额占流通市值比%',
    #     "rzrqyecz": '融资融券余额差值(亿)',
    #
    #     # "sz": 345228341928.120000,  #
    #     # "kcb": 0,
    #     "rqmcl3d": '融券卖出量3d',
    #     "rzmre3d": '融资买入额3d',
    #     "rqjmg3d": '融券净卖股3d',
    #     "rqchl3d": '融券偿还量3d',
    #     "rzche3d": '融资偿还额3d',
    #     "rzjme3d": '融资净买额3d',
    #     "rchange3dcp": '3日涨跌幅',
    #
    #     "rzmre5d": '融资买入额5d',
    #     "rqmcl5d": '融券卖出量5d',
    #     "rqjmg5d": '融券净卖股5d',
    #     "rqchl5d": '融券偿还量5d',
    #     "rzjme5d": '融资净买额5d',
    #     "rzche5d": '融资偿还额5d',
    #     "rchange5dcp": '5日涨跌幅',
    #
    #     "rqjmg10d": '融券净卖股10d',
    #     "rzche10d": '融券偿还量10d',
    #     "rqchl10d": '融券偿还量10d',
    #     "rqmcl10d": '融券偿还量10d',
    #     "rzjme10d": '融资净买额10d',
    #     "rzmre10d": '融资买入额10d',
    #     "rchange10dcp": '10日涨跌幅',
    #
    # }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    }

    url = f'http://api.dataide.eastmoney.com/data/get_rzrq_ggmx?code={stock.symbol}&orderby=date&order=desc&pageindex=1&pagesize=50'

    res = requests.get(url, headers=header)
    data_json = json.loads(res.text)
    max_page = data_json['pages']
    page = data_json['pageindex']
    res_data = data_json['data']
    while all and page < max_page:
        url = url.replace(f'pageindex={page}', f'pageindex={page+1}')
        print(url)
        res = requests.get(url, headers=header)
        data_json = json.loads(res.text)
        page = data_json['pageindex']
        # print(data_json['data'][0])
        res_data.extend(data_json['data'])

        print(f'get page {page}  success')
        time.sleep(1)

    last_res_data = []
    for one_d in res_data:
        res_one = {}
        timeStamp = one_d['date'] / 1000
        timeArray = time.localtime(timeStamp)
        res_one['trade_date'] = time.strftime("%Y-%m-%d", timeArray)
        # res_one['s_code'] = stock_id
        try:
            res_one['spj'] = round(one_d['spj'], 2)
        except:
            res_one['spj'] = 0
            # res_one['secname'] = one_d['secname']
        try:
            res_one['zdf'] = round(one_d['zdf'], 2)
        except:
            res_one['zdf'] = 0
        try:
            res_one['rzyezb'] = round(one_d['rzyezb'], 2)
        except:
            res_one['rzyezb'] = 0
        try:
            res_one['rzmre'] = round(one_d['rzmre'] / 100000000, 4)
        except:
            res_one['rzmre'] = 0
        try:
            res_one['rzche'] = round(one_d['rzche'] / 100000000, 4)
        except:
            res_one['rzche'] = 0
        try:
            res_one['rzjme'] = round(one_d['rzjme'] / 100000000, 4)
        except:
            res_one['rzjme'] = 0
        try:
            res_one['rzye'] = round(one_d['rzye'] / 100000000, 4)
        except:
            res_one['rzye'] = 0
        try:
            res_one['rzrqye'] = round(one_d['rzrqye'] / 100000000, 4)
        except:
            res_one['rzrqye'] = 0
        try:
            res_one['rzrqyecz'] = round(one_d['rzrqyecz'] / 100000000, 4)
        except:
            res_one['rzrqyecz'] = 0
        try:
            res_one['rqye'] = round(one_d['rqye'] / 100000000, 4)
        except:
            res_one['rqye'] = 0
        res_one['rqmcl'] = one_d['rqmcl'] if one_d['rqmcl'] else 0
        res_one['rqchl'] = one_d['rqchl'] if one_d['rqchl'] else 0
        res_one['rqjmg'] = one_d['rqjmg'] if one_d['rqjmg'] else 0
        res_one['rqyl'] = one_d['rqyl'] if one_d['rqyl'] else 0
        try:
            res_one['rqpjcb'] = round(one_d['rqye'] / one_d['rqyl'], 3)  # 融券平均成本
        except:
            res_one['rqpjcb'] = 0
        last_res_data.append(res_one)
    stocks = RzRq.objects.filter(stock=stock).order_by('-trade_date')
    last_date = None
    if stocks:
        last_date = stocks[0].trade_date
    for da in last_res_data:
        if last_date and da['trade_date'] == last_date:
            break
        da['stock'] = stock
        RzRq.objects.create(**da)
    return last_res_data


# 从tushare获取融资融券数据
def get_rzrq_from_tushare(trade_date):
    """从tushare获取融资融券数据 当天全市场数据 """
    pro = ts.pro_api(MY_TOKEN)
    df = pro.query('margin_detail', trade_date=trade_date)
    df.fillna(value=0, inplace=True)
    data = df.to_dict(orient='records')
    return data


# 从tushare获取个股的财务指标数据
def get_finance_quota_from_tushare(code):
    """从tushare获取个股的财务指标数据 请求一次 获取60条左右 """
    pro = ts.pro_api(MY_TOKEN)
    df = pro.fina_indicator(ts_code=code)
    # df.fillna(value=0, inplace=True)
    data = df.to_dict(orient='records')
    return data


# 获取全部的融资融券数据
def get_all_rzrq():
    """数据从 20140922 开始，但是量太多，需要分次获取"""
    try:
        last_rzrq = TuShareRzRq.objects.all().order_by('-trade_date')[0]
        # print(str(last_rzrq.trade_date))
        start = str(last_rzrq.trade_date)
    except:
        start = '20140922'
    if '-' in start:
        start = start.replace('-', '')
    # print(start)
    today = str(datetime.date.today()).replace('-', '')
    while start != today:
        start_day = datetime.datetime.strptime(start, '%Y%m%d') + datetime.timedelta(days=1)
        start = start_day.date().strftime('%Y%m%d')
        data = get_rzrq_from_tushare(start)
        print(start, '----', time.time())
        if not data:
            continue
        for da in data:
            TuShareRzRq.objects.create(**da)
        time.sleep(2)


# 获取市场周成交量
def get_week_sh_sz():
    """获取周 上海 深圳 市场的周成交量  上深成交量"""
    pro = ts.pro_api(MY_TOKEN)
    sz_df = pro.index_daily(ts_code='399001.SZ')
    sh_df = pro.index_daily(ts_code='000001.SH')
    # print(sh_df.columns)
    # print(sh_df.loc[:4, 'amount'])
    c_time = sh_df.loc[0, 'trade_date']
    c_time = '-'.join([c_time[0:4], c_time[-4:-2], c_time[-2:]])
    sz_week = round(sz_df.loc[:4, 'amount'].sum() / 100000, 2)
    sh_week = round(sh_df.loc[:4, 'amount'].sum() / 100000, 2)
    return sz_week, sh_week, sz_week + sh_week, c_time


# 获取个股的交易数据
def get_stock_trade_data(stock):
    ts.set_token(MY_TOKEN)
    day_df = ts.pro_bar(ts_code=stock.ts_code, asset='E', freq='D', adj='qfq')
    day_df.sort_values(by='trade_date', inplace=True)
    day_df['trade_date'] = pd.to_datetime(day_df['trade_date'], format='%Y%m%d')
    print(day_df.shape)
    data = day_df.to_dict(orient='records')
    stocks = TradeData.objects.filter(stock=stock).order_by('-trade_date')
    last_date = None
    if stocks:
        last_date = stocks[0].trade_date
    for da in data:
        da['stock'] = stock
        if last_date and da['trade_date'] == last_date:
            break
        if TradeData.objects.filter(stock=stock, trade_date=da['trade_date']): continue

        TradeData.objects.create(**da)
    return True


# 获取市场每日指标
def get_market_day_quota(today):
    """获取市场成交额中位数"""
    market_day_quota = {'trade_date': today}
    pro = ts.pro_api(MY_TOKEN)
    day = today.replace('-', '')
    df = pro.daily(trade_date=day)
    if df.shape[0] == 0:
        raise Exception('今天没有数据')
    # columns：['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close',
    # 'change', 'pct_chg', 'vol', 'amount']
    # 全市场成交额 (亿)
    all_amount = sum(df['amount']) / 100000
    df['day_up_10']=(df['change']+0.01)/df['pre_close']>0.1
    df['day_low_10']=(df['change']-0.01)/df['pre_close']<-0.1

    market_day_quota['day_up_10'] = sum(df['day_up_10'])
    market_day_quota['day_low_10'] = sum(df['day_low_10'])
    amount_df = df['amount'].dropna()
    # 市场成交额中位数(万元)
    market_day_quota['day_mid_amount'] = numpy.median(amount_df) / 10
    daily_basic = pro.daily_basic(trade_date=day)

    # print(daily_basic.shape)
    # todo 全市场市值(亿)
    total_mv = sum(daily_basic['total_mv']) / 10000
    market_day_quota['total_mv'] = total_mv
    # 全市场换手率
    market_day_quota['turnover_rate'] = all_amount / total_mv
    # todo 全市场流通市值(亿)
    float_mv = sum(daily_basic['circ_mv']) / 10000
    market_day_quota['float_mv'] = float_mv
    # 基于自由流通市值的换手率
    market_day_quota['turnover_rate_f'] = all_amount / float_mv
    # 市场pe中位数
    market_day_quota['day_mid_pe'] = get_median(daily_basic, 'pe')
    market_day_quota['day_mid_pe_ttm'] = get_median(daily_basic, 'pe_ttm')
    market_day_quota['day_mid_pb'] = get_median(daily_basic, 'pb')
    market_day_quota['pb_lt_1'] = daily_basic[daily_basic['pb'] < 1].shape[0]
    print(market_day_quota['trade_date'], '获取成功')
    # print(market_day_quota)
    MarketDayQuota.objects.create(**market_day_quota)
    return True


# 获取个股财务数据
def get_finance_quota_stock(code):
    pro = ts.pro_api(MY_TOKEN)
    # today = str(datetime.date.today()).replace('-', '')
    df = pro.fina_indicator(ts_code=code)
    data = df.to_dict(orient='records')
    # print(data)
    for da in data:
        ss = pd.Series(da)
        ss.dropna(inplace=True)
        ss = dict(ss)
        text = '-'.join([str(i) for i in ss.values()])
        hash = get_md5(text)
        ss['hash'] = hash
        # for i in da.keys():
        #     if da[i] is None:
        #         print(i)
        # ebitda
        FinanceQuota.objects.create(**ss)
    return True


# 获取中位数
def get_median(df, column):
    values = df[column].dropna()
    return numpy.median(values)


# c_time 2019-12-04
# spj 0
# zdf -0.03
# rzyezb 2.12
# rzmre 319.9674
# rzche 311.8813
# rzjme 8.0861
# rzye 9563.9477
# rzrqye 9694.5508
# rzrqyecz 9433.3447
# rqye 130.603
# rqmcl 137320539.0
# rqchl 140785272.0
# rqjmg -3464733.0
# rqyl 1674684989.0
# rqpjcb 7.799

def get_single_market_rzrq(market, all=False):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    }
    # url = 'http://api.dataide.eastmoney.com/data/get_rzrq_lshj?orderby=dim_date&order=desc&pageindex=1&pagesize=50&jsonp_callback=var%20mbrnfSxZ=(x)&rt=52518095'
    if market == 'sh':
        # 上海
        url = 'http://api.dataide.eastmoney.com/data/get_rzrq_lssh?orderby=dim_date&order=desc&pageindex=1&pagesize=50&jsonp_callback=var%20VTKvuGwt=(x)&scdm=007'
    if market == 'sz':
        # 深圳
        url = 'http://api.dataide.eastmoney.com/data/get_rzrq_lssh?orderby=dim_date&order=desc&pageindex=1&pagesize=50&jsonp_callback=var%20VpEOWDet=(x)&scdm=001'
    res = requests.get(url, headers=header)
    head = re.findall(r'(var.*?=)', res.text)[0]
    data_json = json.loads(res.text.replace(head, ''))
    max_page = data_json['pages']
    page = data_json['pageindex']
    res_data = data_json['data']
    while all and page < max_page:
        url = url.replace(f'pageindex={page}', f'pageindex={page+1}')
        # print(url)
        res = requests.get(url, headers=header)
        head = re.findall(r'(var.*?=)', res.text)[0]
        data_json = json.loads(res.text.replace(head, ''))

        page = data_json['pageindex']
        # print(data_json['data'][0])
        res_data.extend(data_json['data'])
        # print(f'get page {page}  success')
        time.sleep(1)

    last_res_data = {}
    for one_d in res_data:
        res_one = {}
        timeStamp = one_d['dim_date'] / 1000
        timeArray = time.localtime(timeStamp)
        trade_date = time.strftime("%Y-%m-%d", timeArray)
        last_res_data[trade_date] = res_one
        try:
            res_one[f'{market}_rzmre'] = round(one_d['rzmre'] / 100000000, 4)
        except:
            res_one[f'{market}_rzmre'] = 0
        try:
            res_one[f'{market}_rzrqye'] = round(one_d['rzrqye'] / 100000000, 4)
        except:
            res_one[f'{market}_rzrqye'] = 0
        try:
            res_one[f'{market}_rqye'] = round(one_d['rqye'] / 100000000, 4)
        except:
            res_one[f'{market}_rqye'] = 0
    return last_res_data


def get_market_rzrq():
    sh = get_single_market_rzrq(market='sh', all=False)
    sz = get_single_market_rzrq(market='sz', all=False)
    for trade_date in sh.keys():
        try:
            sh_r = sh[trade_date]
            sz_r = sz[trade_date]
        except Exception as e:
            print(e)
            continue
        # print('sh_sz')
        try:
            MarketDayQuota.objects.filter(trade_date=trade_date).update(**dict(**sh_r, **sz_r))
            # print('ok')
        except Exception as e:
            print(e)



