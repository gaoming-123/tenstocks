# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--21:48
# desc:
import copy

import pandas

from util import get_float, cut_short_period, get_peak_index, deviation_judge, swing_vol_warning


def trend(df, n: int = 20, period='week'):
    """
    根据均线判断趋势（定性+加强还是减弱）
    趋势是将最后10天的均线平均 再与最后一天价格比较
    :param df:   n周期的均线数据
    :return:
    """
    smooth_k = 0.01
    if period == 'hour':
        smooth_k = 0.005

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
    next_month_boll_up = last_month_df['boll_up']*2-second_month_df['boll_up']
    next_month_boll_low = last_month_df['boll_low']*2-second_month_df['boll_low']
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
    last_week_df=df_week.iloc[-1,:]
    last_close = last_week_df['close']

    risk_rate_income, section = 0, 0
    # 进入观察区的价格浮动比率
    look_k = 0.05
    # 买入价格浮动比率
    k = 0.025
    # 回报风险比
    income_rate_risk = 0
    # boll线，上轨附近，卖出  给出价格区间
    # boll线上轨附近
    if abs(last_close - next_week_up) < next_week_mid * look_k:
        section = (get_float(next_week_up - k * week_boll_mid_df.iloc[-1]),
                   get_float(next_week_up + k * week_boll_mid_df.iloc[-1]))
        # 卖出  收益风险比很小
        income_rate_risk = 0.01
    # boll线下轨 买入 给出买入区间
    if abs(last_close - next_week_low) < week_boll_mid_df.iloc[-1] * look_k:
        section = (get_float(next_week_low - k * week_boll_mid_df.iloc[-1]),
                   get_float(next_week_low + k * week_boll_mid_df.iloc[-1]))
        try:
            income_rate_risk = (next_week_mid - last_close) / (last_close - next_week_low) - 1

        except:
            income_rate_risk = 6
        if income_rate_risk > 5 or -2 < income_rate_risk < -1:
            income_rate_risk = 5

    res = {
        # 本月boll上轨
        'month_boll_up': get_float(next_month_boll_up),
        'month_boll_low': get_float(next_month_boll_low),
        # 下周boll
        'next_week_up': get_float(next_week_up),
        'next_week_mid': get_float(next_week_mid),
        'next_week_low': get_float(next_week_low),
        # 'last_week_high':last_week_df['high'],
        # 'last_week_low':last_week_df['low'],
        'week_boll_sd': week_boll_sd,
        # 风险回报比
        'income_risk': get_float(income_rate_risk),
        # 价格参考区间
        'section': section,
    }
    return res


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
        f'{period}_boll_up': get_float(boll_up),
        f'{period}_boll_low': get_float(boll_low),
        f'{period}_boll_sd': boll_sd,
        f'{period}_close': get_float(last_df['close']),
        f'{period}_high': get_float(last_df['high']),
        f'{period}_low': get_float(last_df['low']),
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
        'value': {'kdj_k': get_float(k_value, 2), 'kdj_D': get_float(d_value, 2)}
    }
    return res


# 判断背离  MACD KDJ 量价 三种
def deviation(df):
    # 1.根据MACD 值
    # 1.1 判断趋势区间
    # 1.2 判断阶段最大值
    # 1.3 计算最大值的差值 给出背离结论
    macd_sign = pandas.DataFrame()
    data_df = copy.deepcopy(df.loc[:, ['trade_date', 'close', 'MACD', 'kdj_K', 'kdj_D', 'vol', 'vol_MA_10', 'swing']])

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

    return deviation_status


def give_advice(res,period='day'):

    trend=res.get('ma_trend')
    # MACD上涨持续 /MACD上涨减弱 /MACD下跌减弱 /MACD下跌持续
    trend_do_on=res.get('trend_go_on')
    # 超买超卖
    buy_sell=res.get('buy_sell')

    advice='等待'
    if trend in ['上涨','盘整'] or trend_do_on in ['MACD上涨持续','MACD上涨减弱','MACD下跌减弱']:
        if period=='hour':
            if buy_sell=='超买':
                advice='卖出(超买)'
            elif buy_sell=='超卖':
                advice='买入(超卖)'
        elif period=='week':
            day_high=float(res.get('day_high'))
            day_low=float(res.get('day_low'))
            if buy_sell=='超买':
                advice='卖出(超买)'
            elif buy_sell=='超卖':
                advice='买入(超卖)'

            # 价格接近boll线上轨
            # 2.5% 的价格浮动
            if day_high > float(res.get('month_boll_up'))*0.975 or day_high> float(res.get('next_week_up'))*0.975 :
                advice='卖出(BOLL)'

            if day_low < float(res.get('month_boll_low'))*1.025 or day_low< float(res.get('next_week_low'))*1.025 :
                advice='买入(BOLL)'

            if res.get('macd_deviation_status')=='上涨MACD背离' or res.get('kdj_deviation_status')=='上涨KDJ背离':# 上涨MACD背离  下跌MACD背离 两种
                advice='卖出(背离)'
            if res.get('macd_deviation_status')=='下跌MACD背离'or res.get('kdj_deviation_status')=='下跌KDJ背离':# 上涨MACD背离  下跌MACD背离 两种
                advice='买入(背离)'
        elif period=='day':


            day_high=float(res.get('day_high'))
            day_low=float(res.get('day_low'))

            if day_high > float(res.get('day_boll_up'))*0.98  :
                advice='卖出(BOLL)'
            if day_low < float(res.get('day_boll_low'))*1.02  :
                advice='买入(BOLL)'
            if res.get('macd_deviation_status')=='上涨MACD背离' or res.get('kdj_deviation_status')=='上涨KDJ背离':# 上涨MACD背离  下跌MACD背离 两种
                advice='卖出(背离)'
            if res.get('macd_deviation_status')=='下跌MACD背离'or res.get('kdj_deviation_status')=='下跌KDJ背离':# 上涨MACD背离  下跌MACD背离 两种
                advice='买入(背离)'

    return advice


