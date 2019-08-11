from tenstocks.settings import BASE_DIR
from .models import A_stocks,Money_out,WeekCompany
import pandas as pd

# 更新A股的股票
def get_all_stocks():
    import tushare as ts
    pro = ts.pro_api('4516ff6d7ad8bd6c3393fc750c46fb2eed9f0ee3996ecc8f656943a1')
    stocks_list = pro.stock_basic(exchange='', list_status='L',
                                  fields='ts_code,symbol,name,area,industry,fullname,enname,'
                                         'market,exchange,curr_type,list_status,list_date,is_hs') # ,delist_date 该字段未要

    for i in range(stocks_list.shape[0]):
        # print(stocks_list.shape)
        stock=stocks_list.iloc[i,:]
        A_stocks.objects.create(**dict(stock))


# 添加历史数据
def add_money_out_data():
    money_out=pd.read_excel(f'{BASE_DIR}/stocks/行业5日资金流.xlsx',encoding='utf-8')
    money_out=money_out.fillna(0)
    # print(money_out)
    for i in range(money_out.shape[0]):
        row=money_out.iloc[i,:]
        row=dict(row)
        Money_out.objects.create(**row)
    company=pd.read_excel(f'{BASE_DIR}/stocks/行业5日公司.xlsx',encoding='utf-8')
    company=company.fillna('')
    for i in range(company.shape[0]):
        row=company.iloc[i,:]
        row=dict(row)
        WeekCompany.objects.create(**row)

