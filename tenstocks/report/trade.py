# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--21:53
# desc:
import datetime
import tushare as ts

from pre_data import *
from config import MY_TOKEN
from strategy import *
from util import get_float

ts.set_token(MY_TOKEN)

def trade_hour(stock_code, asset='E'):
    start_day = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') + datetime.timedelta(days=-70)
    # start_day = datetime.datetime.strptime('2019-01-23', '%Y-%m-%d') + datetime.timedelta(days=-70)
    start_date = start_day.date().strftime('%Y%m%d')
    hour_df = ts.pro_bar(ts_code=stock_code, freq='60min', asset=asset, start_date=start_date, adj='qfq')
    # print(hour_df.shape)
    hour_df.sort_values(by='trade_time', inplace=True)
    # 删除 9:30时刻的数据
    hour_df = hour_df.drop(hour_df[hour_df['trade_time'].map(lambda x: x.endswith('09:30:00'))].index)

    my_KDJ(hour_df)
    my_MACD(hour_df)
    my_MA(hour_df, timeperiod=(20,))
    my_BOLL(hour_df)

    trend_res = trend(hour_df, n=20, period='hour')
    probab_res = probability(hour_df)
    price_res = price_section(hour_df, period='hour')
    res_hour = dict(**price_res, **probab_res, **trend_res)
    advice=give_advice(res_hour,period='hour')
    html_hour=f"""
    <div>
    <div style="color: magenta ;height: 10px"><b>时参考：</b></div>
    <ul>
        <li>KDJ：【{probab_res.get('buy_sell')}】 快值K:{probab_res.get('value').get('kdj_k')}  慢值D:{probab_res.get('value').get('kdj_D')}</li>
        <li>BOLL：<b>{price_res.get('hour_boll_sd')}</b> 区间：【{price_res.get('hour_boll_low')},{price_res.get('hour_boll_up')}】</li>
        <li>交易参考：<b style="color: blue">{advice}</b> 交易区间：({price_res.get('hour_boll_low')},{price_res.get('hour_boll_up')})</li>
    </ul>
</div>
    """
    # return report_body
    return html_hour

def trade_day(stock_code, asset='E'):
    start_day = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') + datetime.timedelta(days=-200)
    start_date = start_day.date().strftime('%Y%m%d')
    day_df = ts.pro_bar(ts_code=stock_code, start_date=start_date, asset=asset, freq='D', adj='qfq')
    day_df.sort_values(by='trade_date', inplace=True)
    my_BOLL(day_df)
    my_MA(day_df)
    my_MA(day_df, item='vol', timeperiod=(10,))
    my_swing(day_df)
    my_MACD(day_df)
    my_KDJ(day_df)
    # day_df.to_csv('kdj.csv')
    price_res = price_section(day_df, period='day')
    trend_res = trend(day_df)
    probab_res = probability(day_df)
    deviation_res = deviation(day_df)

    res_day = dict(**price_res, **probab_res, **trend_res, **deviation_res)
    advice=give_advice(res_day)
    # trend_res.get('ma_trend')
    # trend_res.get('trend_go_on')
    section=''
    if '买入' in advice:
        section_low=get_float(float(price_res.get('day_boll_low'))*0.98)
        section_up=get_float(float(price_res.get('day_boll_low'))*1.02)
        section+=f'交易区间：({section_low},{section_up})'
    elif '卖出' in advice:
        section_low=get_float(float(price_res.get('day_boll_up'))*0.98)
        section_up=get_float(float(price_res.get('day_boll_up'))*1.02)
        section+=f'交易区间：({section_low},{section_up})'
    else:
        pass

    html_day=f"""
    <div>
    <div style="color: magenta;height: 10px"><b>日参考：</b></div>
    <ul>
        <li>趋势：<b style="color: blue">{' ++ '.join(trend_res.values())}</b></li>
        <li>背离：<b style="color: red">{' ++ '.join(deviation_res.values())}</b></li>
        <li>KDJ：【{probab_res.get('buy_sell')}】 快值K:{probab_res.get('value').get('kdj_k')}  慢值D:{probab_res.get('value').get('kdj_D')}</li>
        <li>BOLL：<b>{price_res.get('day_boll_sd')}</b> 区间：【{price_res.get('day_boll_low')},{price_res.get('day_boll_up')}】</li>
        <li>交易参考：<b style="color: blue">{advice}</b> {section}</li>
    </ul>
</div>
    """
    # return report_body
    return html_day


def trade_week(stock_code, asset='E'):
    # df=ts.pro_bar(ts_code='002701.SZ',freq='D', end_date='20190531',adj='qfq',factors=['tor'])
    start_day = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') + datetime.timedelta(days=-1200)
    start_date = start_day.date().strftime('%Y%m%d')
    month_df = ts.pro_bar(ts_code=stock_code, freq='M', asset=asset, adj='qfq')
    month_df.sort_values(by='trade_date', inplace=True)
    my_BOLL(month_df)
    week_df = ts.pro_bar(ts_code=stock_code, start_date=start_date, asset=asset, freq='W', adj='qfq')
    week_df.sort_values(by='trade_date', inplace=True)
    my_BOLL(week_df)
    my_MA(week_df)
    my_MA(week_df, item='vol', timeperiod=(10,))
    my_swing(week_df)
    my_MACD(week_df)
    my_KDJ(week_df)
    price_res = week_price_section(month_df, week_df)
    # print(price_res)
    trend_res = trend(week_df)
    # print(trend_res)
    probab_res = probability(week_df)
    # print(probab_res)
    deviation_res = deviation(week_df)
    # print(deviation_res)
    res_week = dict(**price_res, **probab_res, **trend_res, **deviation_res)
    day_df = ts.pro_bar(ts_code=stock_code, start_date=start_date, asset=asset, freq='D', adj='qfq')
    day_df=day_df.iloc[0,:]
    res_week['day_high']=day_df['high']
    res_week['day_close']=day_df['close']
    res_week['day_low']=day_df['low']
    advice=give_advice(res_week,period='week')

    income_risk = float(price_res.get('income_risk'))

    section = price_res.get('section')
    if section:
        section = f'【{section[0]},{section[1]}】'

    html_week=f"""
    <div><b>现价：</b><b><u>{day_df['close']}</u></b></div>
<div>月价格区间：<b></b>( {price_res.get('month_boll_low')} , {price_res.get('month_boll_up')} )</div>
<div>
    <div style="color: magenta;height: 10px"><b>周参考：</b></div>
    <ul>
        <li>趋势：<b style="color: blue">{' ++ '.join(trend_res.values())}</b></li>
        <li>背离：<b style="color: red">{' ++ '.join(deviation_res.values())}</b></li>
        <li>KDJ：【{probab_res.get('buy_sell')}】 快值K:{probab_res.get('value').get('kdj_k')}  慢值D:{probab_res.get('value').get('kdj_D')}</li>
        <li>BOLL：<b>{price_res.get('week_boll_sd')}</b> 区间：{price_res.get('next_week_low')}--{price_res.get('next_week_mid')}--{price_res.get('next_week_up')}</li>
        <li>(上涨区间/下跌区间)值：{income_risk}</li>
        <li>交易参考：<b style="color: blue">{advice}</b> 交易区间：{section}</li>
    </ul>
</div>
    """
    # return report_body
    return html_week


def stock_check(stock_code, name='个股'):
    header = f"<hr><div>股票名称：<u>{name}</u> 个股代码： <u>{stock_code}</u></div>"
    res_week = trade_week(stock_code)
    res_day = trade_day(stock_code)
    # res_hour = trade_hour(stock_code)
    # report_text = f"{header}{res_week.strip()}{res_day.strip()}{res_hour.strip()}"
    report_text = f"{header}{res_week.strip()}{res_day.strip()}"
    return report_text


def index_check(index_code, name='指数'):
    """对指数进行检查"""
    header=f"<hr><div>指数名称：<u>{name}</u> 指数代码： <u>{index_code}</u></div>"
    res_week = trade_week(index_code, asset='I')
    res_day = trade_day(index_code, asset='I')
    # res_hour = trade_hour(index_code, asset='I')
    # report_text = f"{header}{res_week}{res_day}{res_hour}"
    report_text = f"{header}{res_week}{res_day}"
    return report_text


if __name__ == '__main__':
    res=stock_check('002701.SZ')
    print(res)