# encoding: utf-8
# author:  gao-ming
# time:  2019/7/3--20:52
# desc:

# encoding: utf-8
# author:  gao-ming
# time:  2019/3/17--21:25
# desc:

from sqlalchemy import Column, create_engine, Integer, String, DateTime, Float, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

"""
ts_code	str	TS代码
symbol	str	股票代码
name	str	股票名称
area	str	所在地域
industry	str	所属行业
fullname	str	股票全称
enname	str	英文全称
market	str	市场类型 （主板/中小板/创业板）
exchange	str	交易所代码
curr_type	str	交易货币
list_status	str	上市状态： L上市 D退市 P暂停上市
list_date	str	上市日期
delist_date	str	退市日期
is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通
"""

class A_stocks(Base):
    __tablename__ = 'a_stocks'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    ts_code=Column(String(16),comment='TS代码')
    symbol=Column(String(10),unique=True,comment='股票代码')
    name=Column(String(16),comment='股票名称')
    area=Column(String(16),comment='所在地域')
    industry=Column(String(16),comment='所属行业')
    fullname=Column(String(16),comment='股票全称')
    enname=Column(String(16),comment='英文全称')
    market=Column(String(16),comment='市场类型 （主板/中小板/创业板）')
    exchange=Column(String(16),comment='交易所代码')
    curr_type=Column(String(16),comment='交易货币')
    list_status=Column(String(16),comment='上市状态： L上市 D退市 P暂停上市')
    list_date=Column(String(16),comment='上市日期')
    delist_date=Column(String(16),comment='退市日期')
    is_hs=Column(String(16),comment='是否沪深港通标的，N否 H沪股通 S深股通')

class Financedata(Base):
    id = Column(Integer, primary_key=True)

    pass

# 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')

engine = create_engine('sqlite:///data.db')
# 创建DBSession类型:



def get_session():
    engine = create_engine('sqlite:///data.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def add_industry():
    Base.metadata.create_all(engine)
    session = get_session()
    new_datas = [Industry(ch_name=i[0], en_name=i[1]) for i in db_n]
    session.add_all(new_datas)

    session.commit()
    session.close()
# ss=session.query(Money_out).get(1)
# print(ss.c_time)
# print(ss.cc)
# session.commit()
# session.close()
#
