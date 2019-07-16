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
from scheduler import My_scheduler

logging.basicConfig(filename='logs/log.txt',filemode="a+",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.ERROR)

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
    print(html)
    theme=f'{today}**诊判报告'
    send_res_to_email(contents=html,theme=theme,content_type='html')




if __name__ == '__main__':
    # main()
    scheduler=My_scheduler()
    scheduler.add_job(main,'cron', day_of_week='0-4', hour=20, minute=0, second=0)
    scheduler.start()
