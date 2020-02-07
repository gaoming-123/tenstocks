# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2019-12-03 14:14
# desc: 辅助方法集合


def cut_short_period(index_list):
    # 除去序号值差值小于4的区间
    while 1:
        max_index = len(index_list) - 1
        # 只有一个值  或者以0开头的区间分割index列表
        if max_index == 0 or (index_list[0] == 0 and max_index == 1):
            break
        for k, v in enumerate(index_list):
            if k < max_index:
                if k == 0:
                    if index_list[1] - index_list[0] < 3:
                        del index_list[k + 1]
                    continue
                if index_list[k + 1] - index_list[k] < 4:
                    if k == max_index - 1:
                        # 如果是第一段数据少于4，则只删除index_list[k + 1]
                        del index_list[k + 1]
                    else:
                        del index_list[k + 1]
                        del index_list[k]
                    break
        if max_index + 1 == len(index_list):
            break


def deviation_judge(section_1: tuple, section_2: tuple = None):
    """
    根据价格 和 MACD  kdj_D  来判断是否背离
    以及判断振幅和量能的异常
    :param section_1: 离现在最近的区间  (DateFrame数据,index 列表)
    :param section_2: 倒数第三个区间
    :return:  背离状态
    """
    deviation_status = {}
    if section_2:
        data_df1, peak_index1 = section_1
        up_sign = 1 if data_df1['MACD'].iloc[peak_index1[0]] > 0 else -1
        section_1_close_macd = (data_df1['close'].iloc[peak_index1[0]], data_df1['MACD'].iloc[peak_index1[0]],
                                data_df1['kdj_D'].iloc[peak_index1[0]])
        data_df3, peak_index3 = section_2
        section_2_close_macd = (data_df3['close'].iloc[peak_index3[0]], data_df3['MACD'].iloc[peak_index3[0]],
                                data_df3['kdj_D'].iloc[peak_index3[0]])
        if len(peak_index3) > 1:
            # 判断出最大的macd值的index
            close_macd_list = []
            macd_list = []
            for i in peak_index3:
                close_macd_list.append((data_df3['close'].iloc[i], data_df3['MACD'].iloc[i], data_df3['kdj_D'].iloc[i]))
                macd_list.append(abs(data_df3['MACD'].iloc[i]))
            max_macd = max(macd_list)
            for close_macd in close_macd_list:
                if close_macd[1] == max_macd:
                    section_2_close_macd = close_macd

        # 判断背离
        if (section_1_close_macd[0] - section_2_close_macd[0]) * (
                section_1_close_macd[1] - section_2_close_macd[1]) < 0:
            if up_sign > 0:
                deviation_status['macd_deviation_status'] = '上涨MACD背离'
            else:
                deviation_status['macd_deviation_status'] = '下跌MACD背离'

        if (section_1_close_macd[0] - section_2_close_macd[0]) * (
                section_1_close_macd[2] - section_2_close_macd[2]) < 0:
            if up_sign > 0:
                deviation_status['kdj_deviation_status'] = '上涨KDJ背离'
            else:
                deviation_status['kdj_deviation_status'] = '下跌KDJ背离'
    else:
        data_df1, peak_index = section_1
        up_sign = 1 if data_df1['MACD'].iloc[peak_index[0]] > 0 else -1
        if (data_df1['close'].iloc[peak_index[0]] - data_df1['close'].iloc[peak_index[1]]) * \
                (data_df1['MACD'].iloc[peak_index[0]] - data_df1['MACD'].iloc[peak_index[1]]) < 0:
            if up_sign > 0:
                deviation_status['macd_deviation_status'] = '上涨MACD背离'
            else:
                deviation_status['macd_deviation_status'] = '下跌MACD背离'
        if (data_df1['close'].iloc[peak_index[0]] - data_df1['close'].iloc[peak_index[1]]) * \
                (data_df1['kdj_D'].iloc[peak_index[0]] - data_df1['kdj_D'].iloc[peak_index[1]]) < 0:
            if up_sign > 0:
                deviation_status['kdj_deviation_status'] = '上涨KDJ背离'
            else:
                deviation_status['kdj_deviation_status'] = '下跌KDJ背离'

    # 量能异常 和 振幅异常提示

    warning_res = swing_vol_warning(data_df1)
    if warning_res:
        deviation_status['swing_vol_warning'] = warning_res

    # deviation_status['macd_trend']='MACD 上涨趋势' if up_sign else 'MACD 下跌趋势'

    return deviation_status


def swing_vol_warning(data_df):
    # 量能异常 和 振幅异常提示
    for row in range(data_df.shape[0]):
        row_data = data_df.iloc[row]
        if (row_data['vol'] / row_data['vol_MA_10']) >= 2 and row_data['swing'] > 0.05:
            return f"{row_data['trade_date']}-振幅和量能异常"
        else:
            return None


def get_peak_index(macd_section):
    """

    :param macd_section: 一个macd指标值区间的DataFrame
    :return:  该区间的极值index
    """
    # macd_section=macd_sec['MACD']
    peak_index = []

    # 判断符号
    # macd_section['MACD'].sum()
    for s_i in range(1, macd_section['MACD'].shape[0] - 1):
        # 判断极值 如果 该值与两侧值的差值乘积符号为正，则为极值
        if (macd_section['MACD'].iloc[s_i] - macd_section['MACD'].iloc[s_i - 1]) * (
                macd_section['MACD'].iloc[s_i] - macd_section['MACD'].iloc[s_i + 1]) > 0:
            # 上升找极大值  下跌找极小值
            if (macd_section['MACD'].iloc[s_i] - macd_section['MACD'].iloc[s_i - 1]) * macd_section[
                'MACD'].sum() > 0:  # 剔除凹值
                peak_index.append(s_i)

    # 第一区间的值还在持续变化，那么极值就是第一值
    if not peak_index:
        peak_index.append(0)
    cut_short_period(peak_index)
    return peak_index


def deviation_macd_judge(section_1: tuple, section_2: tuple = None):
    """
    根据价格 和 MACD   来判断是否背离
    以及判断振幅和量能的异常
    :param section_1: 离现在最近的区间  (DateFrame数据,index 列表)
    :param section_2: 倒数第三个区间
    :return:  背离状态
    """
    deviation_status = {}
    if section_2:
        data_df1, peak_index1 = section_1
        up_sign = 1 if data_df1['MACD'].iloc[peak_index1[0]] > 0 else -1
        section_1_close_macd = (data_df1['close'].iloc[peak_index1[0]], data_df1['MACD'].iloc[peak_index1[0]])
        data_df3, peak_index3 = section_2
        section_2_close_macd = (data_df3['close'].iloc[peak_index3[0]], data_df3['MACD'].iloc[peak_index3[0]])
        if len(peak_index3) > 1:
            # 判断出最大的macd值的index
            close_macd_list = []
            macd_list = []
            for i in peak_index3:
                close_macd_list.append((data_df3['close'].iloc[i], data_df3['MACD'].iloc[i], data_df3['kdj_D'].iloc[i]))
                macd_list.append(abs(data_df3['MACD'].iloc[i]))
            max_macd = max(macd_list)
            for close_macd in close_macd_list:
                if close_macd[1] == max_macd:
                    section_2_close_macd = close_macd

        # 判断背离
        if (section_1_close_macd[0] - section_2_close_macd[0]) * (
                section_1_close_macd[1] - section_2_close_macd[1]) < 0:
            if up_sign > 0:
                deviation_status['macd_deviation_status'] = '上涨MACD背离'
            else:
                deviation_status['macd_deviation_status'] = '下跌MACD背离'

    else:
        data_df1, peak_index = section_1
        up_sign = 1 if data_df1['MACD'].iloc[peak_index[0]] > 0 else -1
        if (data_df1['close'].iloc[peak_index[0]] - data_df1['close'].iloc[peak_index[1]]) * \
                (data_df1['MACD'].iloc[peak_index[0]] - data_df1['MACD'].iloc[peak_index[1]]) < 0:
            if up_sign > 0:
                deviation_status['macd_deviation_status'] = '上涨MACD背离'
            else:
                deviation_status['macd_deviation_status'] = '下跌MACD背离'

    # 量能异常 和 振幅异常提示
    warning_res = swing_vol_warning(data_df1)
    if warning_res:
        deviation_status['swing_vol_warning'] = warning_res

    return deviation_status
