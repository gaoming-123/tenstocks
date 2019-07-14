# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--22:10
# desc:
import datetime
import time

from config import MY_STOCKS, INDEX_S
from trade import stock_check, index_check
from util import send_res_to_email, get_complete_html
import logging


logging.basicConfig(filename='logs/log.txt',filemode="a+",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S", level=logging.error)

def main():
    html=''
    count = 0
    for k, stock in MY_STOCKS.items():
        logging.info(stock)
        count += 1
        try:
            report = stock_check(stock, name=k)
            html += report
        except Exception as exp:
            logging.exception(exp)
        if count % 5 == 0:
            time.sleep(50)
    for name, index in INDEX_S.items():
        logging.info(index)
        count += 1
        try:
            report = index_check(index, name=name)
            html += report
        except Exception as exp:
            logging.exception(exp)
        if count % 5 == 0:
            time.sleep(50)
    today=str(datetime.date.today())
    html=get_complete_html(today,html)
    theme=f'{today}**诊判报告'
    send_res_to_email(contents=html,theme=theme,content_type='html')

if __name__ == '__main__':
    main()
