# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2019-12-03 14:20
# desc: 择股文件
import datetime
import time

from .calcu import trade_day, trade_hour, trade_week, pe_pick


# To 挑选股票
def stock_pick(ts_code, asset, period):
    if period == 'hour':
        res = trade_hour(stock_code=ts_code, asset=asset)
    elif period == 'week':
        res = trade_week(stock_code=ts_code, asset=asset)
    else:
        res = trade_day(stock_code=ts_code, asset=asset)
    return res


def deal_period_result(res):
    pass


# To 获取基础字典
def get_base_dict():
    pick_result = {}
    for i in range(-7, 8):
        pick_result[str(i)] = []
    return pick_result


# To 计算分数
def calc_grade(res):
    # 进行评分
    if not res: return
    # 指标字典
    quota_dict = {
        'deviation': {
            '下跌背离': 4,
            '上涨背离': -4,
        },
        'boll': {
            'boll买入': 2,
            'boll卖出': -2,
        },
        'kdj': {
            '超卖': 1,
            '超买': -1,
        },
    }
    grade = 0
    for quota in quota_dict.keys():
        quota_value = res.get(quota)
        if quota_value:
            for key in quota_dict[quota].keys():
                if key in quota_value:
                    try:
                        if not grade:
                            grade += quota_dict[quota][key]
                        else:
                            g = quota_dict[quota][key]
                            if grade * g > 0:
                                grade += g
                    except:
                        pass
    return grade


def pick_buy_or_sell(stocks, period: str):
    is_str = isinstance(stocks[0], str)
    # 挑选可操作的股票
    pick_result = get_base_dict()
    for stock in stocks:
        try:
            if not is_str:
                stock = stock.ts_code
            print(f'开始：{stock}')
            res = stock_pick(stock, asset='E', period=period)
            grade = calc_grade(res)
            print('结束：',stock)
            if grade:
                pick_result[str(grade)].append(stock)
            time.sleep(0.5)
        except Exception as e:
            print(e)
    return pick_result


# To 挑选可买入股票
def pick_buy(stocks, period: str):
    pick_result = {}
    for i in range(1, 8):
        pick_result[str(i)] = []
    if not isinstance(stocks[0], str):
        stocks = [stock.ts_code for stock in stocks]
    for stock in stocks:
        buy = 0
        try:
            res = stock_pick(stock, asset='E', period=period)
            if res:
                print(res)
                deviation = res.get('deviation')
                if deviation and '下跌' in deviation:
                    buy += 4
                boll = res.get('boll')
                if boll and '买入' in boll:
                    buy += 2
                kdj = res.get('kdj')
                if kdj and '超卖' in kdj:
                    buy += 1
            print(stock)
            if buy:
                pick_result[str(buy)].append((stock.ts_code, stock.name))
            time.sleep(0.5)
        except Exception as e:
            print(e)
    return pick_result

# pe<15 and Boll下轨附近
def PE15BollPick():
    today = str(datetime.date.today()).replace('-', '')
    stocks = pe_pick(date_day=today,pe=15)
    print(len(stocks))
    for stock in stocks:
        try:
            print(f'开始：{stock}')
            res = stock_pick(stock, asset='E', period='week')

        except Exception as e:
            print(e)
    for ke in res.keys():
        print(ke, len(res[ke]))
