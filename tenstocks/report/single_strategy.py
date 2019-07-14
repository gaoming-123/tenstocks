# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--22:02
# desc:

def stragtegy_MACD(df):
    macd_df = df[['DIF', 'DEA', 'MACD']]
    macd_list = df['MACD']
    # var_macd_list=[]
    # i=1
    # while 1:
    #     var_macd=macd_list[-i]-macd_list[-1-1]
    #     var_macd_list.append(var_macd)
    last_macd = macd_df.iloc[-1, :]
    last_DIF = last_macd['DIF']
    last_DEA = last_macd['DEA']
    last_MACD = last_macd['MACD']
    up_trend = False
    if last_DIF > last_DEA and last_MACD > 0:
        up_trend = '上升趋势'
    else:
        up_trend = '震荡或下降趋势'
    var_macd_mark = []

    for i in range(1, len(macd_list)):
        var_macd = macd_list[-i] - macd_list[-i - 1]
        if i == 1:
            try:
                first_mark = var_macd / abs(var_macd)
            except:
                first_mark = 0
        if var_macd > 0:
            var_macd_mark.append(1)
        elif var_macd < 0:
            var_macd_mark.append(-1)
        else:
            var_macd_mark.append(0)
        i += 1
    if first_mark == 1:
        trend_add = '增强'
    else:
        trend_add = '减弱'

    res = {
        'trend': up_trend + '--' + trend_add,
    }
    return res


def strategy_BOLL(df, n: int = 20):
    """
    判断价格边界 价格运动 有一定的边界
    :param df:
    :param n:  使用的数据长度  默认20
    :return:   上下轨价格  以及 在上轨或下轨附近，给出操作的价格区间  其它为0
    """
    boll_df = df.iloc[-n:, :]
    mid_s = boll_df['boll_mid']
    last_mid = mid_s[-1]
    # 计算下一周期的boll轨道
    next_mid = mid_s[-1] * 2 - mid_s[-2]
    next_up = boll_df['boll_up'][-1] * 2 - boll_df['boll_up'][-2]
    next_dn = boll_df['boll_dn'][-1] * 2 - boll_df['boll_dn'][-2]
    last_close = df['close'][-1]
    risk_rate_income, section = 0, 0
    # boll线，上轨附近，卖出  给出价格区间
    if abs(last_close - next_up) < last_mid * 0.025:
        section = (next_up - 0.025 * last_mid, next_up + 0.025 * last_mid)
        # 卖出  收益风险比很小
        risk_rate_income = 0.01
    # boll线下轨 买入 给出买入区间
    if abs(last_close - next_dn) < last_mid * 0.025:
        section = (next_dn - 0.025 * last_mid, next_dn + 0.025 * last_mid)
        try:
            risk_rate_income = (next_mid - last_close) / (last_close - next_dn) - 1
        except:
            risk_rate_income = 6
        if risk_rate_income > 5 or risk_rate_income < -1:
            risk_rate_income = 5
    res = {
        'next_up': next_up,
        'next_dn': next_dn,
        # 风险回报比
        'risk_income': '%.2f' % risk_rate_income,
        # 价格参考区间
        'section': section,
    }
    return res


def strategy_KDJ(df):
    """
    判断概率边界  超买 跌的概率大    超卖  涨的概率大
    :param df:
    :return:
    """
    kdj_df = df[['kdj_K', 'kdj_D']]
    kdj_df['K-D'] = kdj_df['kdj_K'] - kdj_df['kdj_D']
    last_kdj = kdj_df.iloc[-1, :]
    kdj_K = last_kdj['kdj_K']
    kdj_D = last_kdj['kdj_D']
    too_much = False
    if kdj_K > 80 or kdj_D > 80:
        too_much = '进入超买区间'
    if kdj_K < 20 or kdj_D < 20:
        too_much = '进入超卖区间'
    res = {
        'kdj_K': kdj_K,
        'kdj_D': kdj_D,
    }
    if too_much:
        res['kdj_res'] = too_much

    return res


def strategy_RSI(df):
    rsi_df = df[['RSI_6', 'RSI_12', 'RSI_24']]

    pass


def strategy_MA(df, n: int = 20):
    """
    均线策略，判断趋势
    :param df:
    :return:
    """
    try:
        ma_df = df[f'close_MA_{n}']
    except Exception as e:
        raise Exception('均线周期或数据有误！')
    # 上升趋势，平盘，下降趋势，最后返回的趋势结果
    # mark_up,mark_line,mark_dn,trend=0,0,0,0

    # print('0',mark_up)
    # boll中线的波动值边界，在这个值内波动，认为是合理的波动
    stand_value = ma_df[-1] * 0.007
    var_mid_list = []
    var_mid_mark = []
    for i in range(2, n):
        # 计算boll中线前后差值
        var_mid = ma_df[-i] - ma_df[1 - i]
        var_mid_list.append(var_mid)
        # 判断趋势
        if abs(var_mid) < stand_value:
            mark = 0  # 平盘
        elif var_mid > stand_value:
            mark = 1  # 上升趋势
        else:
            mark = -1  # 下降趋势
        var_mid_mark.append(mark)

    last_mark = var_mid_mark[0]
    # 保存趋势，以及加强还是减弱
    trend_res = [last_mark, -1]
    if var_mid_mark[0] * var_mid_mark[1] > 0:
        if abs(var_mid_list[0]) > abs(var_mid_list[1]):
            trend_res[1] = 1  # 趋势加强
    # 判断趋势延续的周期
    trend_num = 0
    for i in range(1, n):
        trend_num += 1
        if var_mid_list[i] * var_mid_list[i - 1] < 0:
            break

    suggest = '清仓' if last_mark == -1 else '持仓或波段'
    trend_dict = {
        '1': '上升',
        '0': '平盘',
        '-1': '下降',
    }
    trend_add = {
        '-1': '减弱',
        '1': '加强',
    }
    trend_judge = trend_dict[trend_res[0]] + '  ' + trend_add[trend_res[1]]
    res = {
        'suggest': suggest,
        # 趋势
        'trend': trend_judge,
        # 周期持续的长度
        'trend_num': trend_num,
    }
    return res


def strategy_VOL(df):
    """
    根据成交量来判断
    :param df:含有成交量 和成交量均值的dataframe
    :return:  判断结果:
        'abnormal':量能是否异常,
        'vol_status':量能增减状态,
        'period':持续时间,
    """
    vol_df = df[['vol', 'vol_MA_10']]
    # 判断量能异常
    vol_abnormal = 0
    last_vol = vol_df[-1, :]
    if last_vol['vol'] / last_vol['vol_MA_10'] > 2:
        vol_abnormal = '量能异常'
    # 记录成交量的增减状态
    var_vol_MA_sign = []
    for i in range(1, 50):
        last_vol = vol_df[-i, :]
        if last_vol['vol'] - last_vol['vol_MA_10'] >= 0:
            var_vol_MA_sign.append(1)
        else:
            var_vol_MA_sign.append(-1)
    if var_vol_MA_sign[0] == 1:
        vol_status = '量能增加'
    else:
        vol_status = '量能减少'
    # 保存变化的节点index
    change_index = []
    #
    for i in range(len(var_vol_MA_sign)):
        if var_vol_MA_sign[i] * var_vol_MA_sign[i + 1] < 0:
            change_index.append(i)
    # 量能交替不能超过3个周期，否则持续状态结束
    i = 0
    while 1:
        if change_index[i + 1] - change_index[i] > 3:
            vol_period = i
            break
        i += 2
    vol_period = change_index[vol_period]

    res = {
        'abnormal': vol_abnormal,
        'vol_status': vol_status,
        'period': vol_period,
    }
    return res
