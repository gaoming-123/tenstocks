# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--21:45
# desc:
import talib


def my_MACD(df, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    :param data: 包含收盘价的Dataframe
    :param fastperiod: 快线周期参数 默认：12
    :param slowperiod: 慢线周期参数 默认：26
    :param signalperiod: 信号周期参数 默认：9
    :return: DataFrame
    """
    DIF, DEA, MACD_1 = talib.MACD(df['close'].values,
                                  fastperiod=fastperiod,
                                  slowperiod=slowperiod,
                                  signalperiod=signalperiod)
    df['DIF'], df['DEA'], df['MACD'] = DIF, DEA, MACD_1 * 2
    return df


def my_BOLL(df, timeperiod=20, nbdevup=2, nbdevdn=2):
    """
    :param data: 包含收盘价的Dataframe
    :param timeperiod: 时间周期参数 如：20
    :param nbdevup: 上轨标准差倍数 默认：2
    :param nbdevdn: 下轨标准差倍数 默认：2
    :return:  Dataframe
    """
    # df = pd.DataFrame()
    df['boll_up'], df['boll_mid'], df['boll_low'] = talib.BBANDS(df['close'].values,
                                                                 timeperiod=timeperiod,
                                                                 nbdevup=nbdevup,
                                                                 nbdevdn=nbdevdn)
    # 两倍标准差
    df['boll_SD'] = df['boll_up'] - df['boll_mid']
    return df


def my_RSI(df, timeperiod: tuple = (6, 12, 24)):
    """
    应用中一般要使用三次 6、12、24
    :param data: 包含收盘价的Dataframe
    :param timeperiod: 参数 例如6、12、24
    :return:  Dataframe
    """
    for i in timeperiod:
        df[f'RSI_{i}'] = talib.RSI(df['close'].values, timeperiod=i)
    return df


def my_KDJ(df, fastk_period=9, slowk_period=3, slowd_period=3):
    """
    此处KDJ与 同花顺的指标值有差异
    :param data: 包含最高价、最低价、收盘价的Dataframe
    :param fastk_period: kdj参数 默认就可以
    :param slowk_period: kdj参数 默认就可以
    :param slowd_period: kdj参数 默认就可以
    :return: 包含 K、D值的Dataframe
    """
    df['kdj_K'], df['kdj_D'] = talib.STOCH(df['high'].values,
                                           df['low'].values,
                                           df['close'].values,
                                           fastk_period=fastk_period,
                                           slowk_period=slowk_period,
                                           slowk_matype=0,
                                           slowd_period=slowd_period,
                                           slowd_matype=0)

    return df


def my_MA(df, item='price', timeperiod: tuple = (20,)):
    """
    :param data:  包含收盘价的Dataframe
    :param timeperiod: 均线的参数  例如(5,10,20)
    :return: Dataframe
    """
    item = 'close' if item == 'price' else 'vol'
    t_list = list(timeperiod)
    for i in t_list:
        df[f'{item}_MA_{i}'] = talib.MA(df[item].values, timeperiod=i)
    return df


def my_swing(df):
    """
    振幅计算
    :param df: 包含最高价，最低价，昨日价的Dataframe
    :return:
    """
    df['swing'] = (df['high'] - df['low']) / df['pre_close']
    return df

