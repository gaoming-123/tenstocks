# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--22:10
# desc:
import datetime
import time

from trade import stock_check, index_check
from util import send_res_to_email, get_complete_html,get_index,get_stocks
import logging
from scheduler import My_scheduler

logging.basicConfig(filename='logs/log.txt',filemode="a+",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

def main():
    html=''
    count = 0
    MY_STOCKS=get_stocks()

    for item in MY_STOCKS:
        k,stock=item.split(':')
        # logging.info(stock)
        count += 1
        try:
            report = stock_check(stock, name=k)
            html += report
            logging.info(stock)
        except Exception as exp:
            logging.exception(exp)
        if count % 4 == 0:
            time.sleep(60)
    INDEX_S=get_index()
    for ind in INDEX_S:
        name,index=ind.split(':')
        # logging.info(index)
        count += 1
        try:
            report = index_check(index, name=name)
            html += report
            logging.info(index)
        except Exception as exp:
            logging.exception(exp)
        if count % 4 == 0:
            time.sleep(60)
    today=str(datetime.date.today())
    html=get_complete_html(today,html)
    #print(html)
    theme=f'{today}**诊判报告'
    send_res_to_email(contents=html,theme=theme,content_type='html')




if __name__ == '__main__':
    #main()
    scheduler=My_scheduler()
    scheduler.add_job(main,'cron', day_of_week='0,1,2,3,5,6', hour=20, minute=1, second=0)
    scheduler.start()
