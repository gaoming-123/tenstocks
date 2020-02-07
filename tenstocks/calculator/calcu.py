# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2019-12-03 14:22
# desc: 计算文件
import copy
import datetime
import pandas

import tushare as ts
from .utils import cut_short_period, get_peak_index, deviation_judge, swing_vol_warning, deviation_macd_judge
from .pretreatment import *
from .config import MY_TOKEN

ts.set_token(MY_TOKEN)


# 趋势
def trend(df, n: int = 20, period='week'):
    """
    根据均线判断趋势（定性+加强还是减弱）
    趋势是将最后10天的均线平均 再与最后一天价格比较
    :param df:   n周期的均线数据
    :return:
    """
    smooth_k = 0.006
    if period == 'hour':
        smooth_k = 0.004

    # 1. 根据20周均线 计算出趋势状态 上涨 平盘 下跌
    column_name = f'close_MA_{n}'
    ma_n_df = df[column_name]
    # 10个n日均线值的均值
    ma_n_10_mean = ma_n_df[-10:].mean()
    last_ma_n = ma_n_df.iloc[-1]
    # 趋势判断
    if last_ma_n > ma_n_df.iloc[-2]:
        # print(last_ma_n,ma_n_10_mean)
        ma_trend = '上涨'
    else:
        ma_trend = '下跌'
    if abs(last_ma_n - ma_n_10_mean) / ma_n_10_mean < smooth_k:
        ma_trend = '盘整'
    ## 2. 根据MACD值 判断趋势延续性 以及反转的可能性
    macd_df = df['MACD']
    last_macd = macd_df.iloc[-1]
    second_macd = macd_df.iloc[-2]
    if last_macd > 0:
        if last_macd - second_macd > 0:
            trend_go_on = 'MACD上涨持续'
        else:
            trend_go_on = 'MACD上涨减弱'
    else:
        if last_macd - second_macd > 0:
            trend_go_on = 'MACD下跌减弱'
        else:
            trend_go_on = 'MACD下跌持续'
    res = {
        'ma_trend': ma_trend,
        'trend_go_on': trend_go_on
    }
    return res


# 月、周价格区间
def week_price_section(df_month, df_week):
    """
    根据boll来判断价格区间
    :param df_month:
    :param df_week:
    :return:
    """
    # 1. 月线boll线上下轨
    last_month_df = df_month.iloc[-1, :]
    second_month_df = df_month.iloc[-2, :]
    next_month_boll_up = last_month_df['boll_up'] * 2 - second_month_df['boll_up']
    next_month_boll_low = last_month_df['boll_low'] * 2 - second_month_df['boll_low']
    # 2. 周线boll线上下轨 标准差收敛情况
    week_boll_up_df = df_week['boll_up']
    week_boll_low_df = df_week['boll_low']
    week_boll_mid_df = df_week['boll_mid']
    # 计算收敛情况
    week_boll_sd_df = df_week['boll_SD']
    sd_mean = week_boll_sd_df[-10:].mean()
    # print(sd_mean)
    week_boll_sd = '正常'
    if week_boll_sd_df.iloc[-1] > sd_mean:
        week_boll_sd = '发散'
    if week_boll_sd_df.iloc[-1] < sd_mean:
        week_boll_sd = '收敛'
    # 计算下一周的boll上下轨价格
    next_week_up = week_boll_up_df.iloc[-1] * 2 - week_boll_up_df.iloc[-2]
    next_week_low = week_boll_low_df.iloc[-1] * 2 - week_boll_low_df.iloc[-2]
    next_week_mid = week_boll_mid_df.iloc[-1] * 2 - week_boll_mid_df.iloc[-2]

    # 3. 计算周线boll线上轨附近卖出价格区间  下轨附近买入区间
    last_week_df = df_week.iloc[-1, :]
    last_close = last_week_df['close']

    risk_rate_income, section = 0, 0
    # 进入观察区的价格浮动比率
    look_k = 0.03 - last_close / 10000 * 2
    look_k = look_k if look_k > 0.01 else 0.01
    # 买入价格浮动比率
    k = look_k / 2
    # 回报风险比
    income_rate_risk = 0
    # boll线，上轨附近，卖出  给出价格区间
    # boll线上轨附近
    if abs(last_close - next_week_up) < next_week_mid * look_k:
        section = (round(next_week_up - k * week_boll_mid_df.iloc[-1], 2),
                   round(next_week_up + k * week_boll_mid_df.iloc[-1], 2))
        # 卖出  收益风险比很小
        income_rate_risk = 0.01
    # boll线下轨 买入 给出买入区间
    if abs(last_close - next_week_low) < week_boll_mid_df.iloc[-1] * look_k:
        section = (round(next_week_low - k * week_boll_mid_df.iloc[-1], 2),
                   round(next_week_low + k * week_boll_mid_df.iloc[-1], 2))
        try:
            income_rate_risk = (next_week_mid - last_close) / (last_close - next_week_low) - 1

        except:
            income_rate_risk = 6
        if income_rate_risk > 5 or -2 < income_rate_risk < -1:
            income_rate_risk = 5

    res = {
        # 本月boll上轨
        'month_boll_up': round(next_month_boll_up, 2),
        'month_boll_low': round(next_month_boll_low, 2),
        # 下周boll
        'next_week_up': round(next_week_up, 2),
        'next_week_mid': round(next_week_mid, 2),
        'next_week_low': round(next_week_low, 2),
        # 'last_week_high':last_week_df['high'],
        # 'last_week_low':last_week_df['low'],
        'week_boll_sd': week_boll_sd,
        # 风险回报比
        'income_risk': round(income_rate_risk, 2),
        # 价格参考区间
        'section': section,
    }
    return res


# 价格区间
def price_section(df, period: str):
    """
    获取某个周期的boll上下轨的值 以及 收敛情况
    :param df: 包含boll数据 的DateFrame
    :param period: 自定义周期
    :return:  返回boll上下轨的值 及 收敛情况
    """
    last_df = df.iloc[-1, :]
    boll_up = last_df['boll_up']
    boll_low = last_df['boll_low']

    boll_sd_df = df['boll_SD']
    sd_mean = boll_sd_df[-10:].mean()
    # print(sd_mean)
    boll_sd = '正常'
    if boll_sd_df.iloc[-1] > sd_mean:
        boll_sd = '发散'
    if boll_sd_df.iloc[-1] < sd_mean:
        boll_sd = '收敛'
    return {
        f'{period}_boll_up': round(boll_up, 2),
        f'{period}_boll_low': round(boll_low, 2),
        f'{period}_boll_sd': boll_sd,
        f'{period}_close': round(last_df['close'], 2),
        f'{period}_high': round(last_df['high'], 2),
        f'{period}_low': round(last_df['low'], 2),
    }


# 根据kdj来判断概率
def probability(df):
    # 1. kdj指标 K、D的值与20 80 比较 给出超买 超卖结论
    last_kdj = df.iloc[-1, :]
    k_value = last_kdj['kdj_K']
    d_value = last_kdj['kdj_D']
    buy_sell = '合理'
    if d_value > 80 or k_value > 80:
        buy_sell = '超买'
    if d_value < 20 or k_value < 20:
        buy_sell = '超卖'
    res = {
        'buy_sell': buy_sell,
        'value': {'kdj_k': round(k_value, 2), 'kdj_D': round(d_value, 2)}
    }
    return res


# 判断背离  MACD KDJ 量价 三种
def deviation(df):
    # 1.根据MACD 值
    # 1.1 判断趋势区间
    # 1.2 判断阶段最大值
    # 1.3 计算最大值的差值 给出背离结论
    macd_sign = pandas.DataFrame()
    data_df = copy.deepcopy(
        df.reindex(columns=['trade_date', 'close', 'MACD', 'kdj_K', 'kdj_D', 'vol', 'vol_MA_10', 'swing']))

    data_df.dropna(axis=0, inplace=True)
    data_df.sort_index(ascending=True, inplace=True)
    # MACD的正负符号
    macd_sign['MACD_sign'] = data_df['MACD'] / abs(data_df['MACD'])

    # 记录macd符号变化的index
    sign_change_index = [0, ]
    for i in range(macd_sign.shape[0] - 1):
        if data_df['MACD'].iloc[i] * data_df['MACD'].iloc[i + 1] < 0:
            sign_change_index.append(i)
    # print(sign_change_index)
    # 进行小于4的区间去除
    cut_short_period(sign_change_index)
    # print(sign_change_index)
    try:
        data_section_1 = data_df.iloc[0:sign_change_index[1] + 1]
        # 将分区代码简化
        # n=4
        # for _ in range(1,n):
        #     section_name=f'macd_section_{_}'
        #     section_name=data_df.iloc[sign_change_index[_-1]:sign_change_index[_]+1]
        # print(data_section_1)
        section_2_length = sign_change_index[2] - sign_change_index[1]
        # 找极值
        peak_index = get_peak_index(data_section_1)

        # 如果第一个区间有多个极值，就可以直接判断背离
        if len(peak_index) > 1:
            deviation_status = deviation_judge((data_section_1, peak_index))
        elif section_2_length > 10:
            # 当第二个区间太长，就失去判断背离的时间基础
            deviation_status = {}
            waring_res = swing_vol_warning(data_section_1)
            if waring_res:
                deviation_status['swing_vol_warning'] = waring_res
        else:
            # 否则，需要倒数 1,3两个区间进行判断
            data_section_3 = data_df.iloc[sign_change_index[2] + 1:sign_change_index[3] + 1]
            # print(macd_section_3)
            peak_index_3 = get_peak_index(data_section_3)

            deviation_status = deviation_judge((data_section_1, peak_index), (data_section_3, peak_index_3))
            # print(deviation_status)
    except:
        deviation_status = {}
    return deviation_status


# macd背离
def deviation_macd(df):
    # 1.根据MACD 值
    # 1.1 判断趋势区间
    # 1.2 判断阶段最大值
    # 1.3 计算最大值的差值 给出背离结论
    macd_sign = pandas.DataFrame()
    data_df = copy.deepcopy(df.reindex(columns=['trade_date', 'close', 'MACD', 'vol', 'vol_MA_10', 'swing']))

    data_df.dropna(axis=0, inplace=True)
    data_df.sort_index(ascending=True, inplace=True)
    # MACD的正负符号
    macd_sign['MACD_sign'] = data_df['MACD'] / abs(data_df['MACD'])

    # 记录macd符号变化的index
    sign_change_index = [0, ]
    for i in range(macd_sign.shape[0] - 1):
        if data_df['MACD'].iloc[i] * data_df['MACD'].iloc[i + 1] < 0:
            sign_change_index.append(i)
    # print(sign_change_index)
    # 进行小于4的区间去除
    cut_short_period(sign_change_index)
    # print(sign_change_index)

    data_section_1 = data_df.iloc[0:sign_change_index[1] + 1]
    # 将分区代码简化
    # n=4
    # for _ in range(1,n):
    #     section_name=f'macd_section_{_}'
    #     section_name=data_df.iloc[sign_change_index[_-1]:sign_change_index[_]+1]
    print(data_section_1)
    section_2_length = sign_change_index[2] - sign_change_index[1]
    # 找极值
    peak_index = get_peak_index(data_section_1)

    # 如果第一个区间有多个极值，就可以直接判断背离
    if len(peak_index) > 1:
        deviation_status = deviation_macd_judge((data_section_1, peak_index))
    elif section_2_length > 10:
        # 当第二个区间太长，就失去判断背离的时间基础
        deviation_status = {}
        waring_res = swing_vol_warning(data_section_1)
        if waring_res:
            deviation_status['swing_vol_warning'] = waring_res
    else:
        # 否则，需要倒数 1,3两个区间进行判断
        data_section_3 = data_df.iloc[sign_change_index[2] + 1:sign_change_index[3] + 1]
        # print(macd_section_3)
        peak_index_3 = get_peak_index(data_section_3)

        deviation_status = deviation_macd_judge((data_section_1, peak_index), (data_section_3, peak_index_3))
        # print(deviation_status)

    return deviation_status


def pe_pick(date_day=None,pe=50):
    pro = ts.pro_api(MY_TOKEN)
    df=pandas.DataFrame()
    if date_day is None:
        while df.empty:
            date_day=str(datetime.date.today())
            start_day = datetime.datetime.strptime(date_day, '%Y-%m-%d') + datetime.timedelta(days=-1)
            date_day = start_day.date().strftime('%Y%m%d')
            df = pro.daily_basic(trade_date=date_day)
    else:
        df = pro.daily_basic(trade_date=date_day)
    print(df.shape)
    df = df.loc[(df['pe'] < pe) & (df['pe_ttm'] < pe), ['ts_code']]
    return [i for i in df['ts_code']]

# 背离挑选
def deviation_pick(deviation_res):
    result = {}
    deviation_status = deviation_res.get('macd_deviation_status') if deviation_res.get(
        'macd_deviation_status') else deviation_res.get('kdj_deviation_status')
    if deviation_status:
        if '上涨' in deviation_status:
            result['deviation'] = '上涨背离'
        else:
            result['deviation'] = '下跌背离'
    return result


# boll挑选
def boll_pick(price_res, period: str):
    period_dict={
        'hour':0.005,
        'day':0.01,
        'week':0.02,
        'month':0.03,
    }
    result = {}
    boll_up = price_res.get(f'{period}_boll_up')
    boll_low = price_res.get(f'{period}_boll_low')
    close = price_res.get(f'{period}_close')
    high = price_res.get(f'{period}_high')
    low = price_res.get(f'{period}_low')
    k=period_dict.get(period)
    # if boll_up - high < close * k:
    if boll_up - close < close * k:
        result['boll'] = f'{period}boll卖出'
    # if low - boll_low < close * k:
    if close - boll_low < close * k:
        result['boll'] = f'{period}boll买入'
    return result


# kdj挑选
def kdj_pick(probab_res):
    buy_sell = probab_res.get('buy_sell')
    return {'kdj': buy_sell if buy_sell else ''}


# 返回挑选结果(每个个股，对应周期)
def trade_period_return(deviation_res, price_res, probab_res, period):
    deviation_status = deviation_pick(deviation_res)
    boll_status = boll_pick(price_res, period=period)
    kdj_status = kdj_pick(probab_res)
    return dict(**deviation_status, **boll_status, **kdj_status)


# 天计算
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
    if trend_res.get('ma_trend') == '下跌':
        return False
    return trade_period_return(deviation_res, price_res, probab_res, period='day')


# 周计算
def trade_week(stock_code, asset='E'):
    # df=ts.pro_bar(ts_code='002701.SZ',freq='D', end_date='20190531',adj='qfq',factors=['tor'])
    start_day = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') + datetime.timedelta(days=-1200)
    start_date = start_day.date().strftime('%Y%m%d')
    # month_df = ts.pro_bar(ts_code=stock_code, freq='M', asset=asset, adj='qfq')
    # month_df.sort_values(by='trade_date', inplace=True)
    # my_BOLL(month_df)
    week_df = ts.pro_bar(ts_code=stock_code, start_date=start_date, asset=asset, freq='W', adj='qfq')
    week_df.sort_values(by='trade_date', inplace=True)
    my_BOLL(week_df)
    my_MA(week_df)
    my_MA(week_df, item='vol', timeperiod=(10,))
    my_swing(week_df)
    my_MACD(week_df)
    my_KDJ(week_df)
    price_res = price_section(week_df, period='week')
    # print(price_res)
    trend_res = trend(week_df)
    # print(trend_res)
    probab_res = probability(week_df)
    # print(probab_res)
    deviation_res = deviation(week_df)
    # print(deviation_res)
    if trend_res.get('ma_trend') == '下跌':
        return False
    return trade_period_return(deviation_res, price_res, probab_res, period='week')


# 小时计算
def trade_hour(stock_code, asset='E'):
    start_day = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') + datetime.timedelta(days=-70)
    start_date = start_day.date().strftime('%Y%m%d')
    hour_df = ts.pro_bar(ts_code=stock_code, freq='60min', asset=asset, start_date=start_date, adj='qfq')
    # print(hour_df.shape)
    hour_df.sort_values(by='trade_time', inplace=True)
    # 删除 9:30时刻的数据
    hour_df = hour_df.drop(hour_df[hour_df['trade_time'].map(lambda x: x.endswith('09:30:00'))].index)

    my_KDJ(hour_df)
    my_MACD(hour_df)
    my_MA(hour_df, timeperiod=(20, 60))
    my_BOLL(hour_df)
    my_MA(hour_df, item='vol', timeperiod=(10,))
    my_swing(hour_df)
    trend_res_20 = trend(hour_df, n=20, period='hour')
    trend_res_60 = trend(hour_df, n=60, period='hour')
    probab_res = probability(hour_df)
    price_res = price_section(hour_df, period='hour')
    deviation_res = deviation(hour_df)
    if trend_res_20.get('ma_trend') == '下跌' and trend_res_60.get('ma_trend') == '下跌':
        return False

    return trade_period_return(deviation_res, price_res, probab_res, period='hour')


if __name__ == '__main__':
    pe_pick()
