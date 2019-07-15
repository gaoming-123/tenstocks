# encoding: utf-8
# author:  gao-ming
# time:  2019/7/15--20:22
# desc:

# 参考文章
# https://blog.csdn.net/zhh_love123/article/details/88575598

# from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


# 配置作业存储器
# 如果你的应用在每次启动的时候都会重新创建作业，那么使用默认的作业存储器（MemoryJobStore）即可，
# 但是如果你需要在调度器重启或者应用程序奔溃的情况下任然保留作业，你应该根据你的应用环境来选择具体的作业存储器。

class My_scheduler():
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.port = 27017
        # self.client = MongoClient()
        self.jobstores = {
            # 'mongo': MongoDBJobStore(collection='job', database='school', client=client),
            'default': MemoryJobStore()
        }
        # 配置执行器，并设置线程数
        self.executors = {
            'default': ThreadPoolExecutor(10),
            'processpool': ProcessPoolExecutor(3)
        }
        self.job_defaults = {
            'coalesce': False,  # 默认情况下关闭新的作业
            'max_instances': 3  # 设置调度程序将同时运行的特定作业的最大实例数3
        }
        self.scheduler = BlockingScheduler(jobstores=self.jobstores, executors=self.executors,
                                           job_defaults=self.job_defaults)

    def add_job(self, job, *args, **kwargs):
        # self.scheduler.add_job(my_job, 'cron', day_of_week='mon-fri', hour=20, minute=0, secend=0)
        self.scheduler.add_job(job, *args, **kwargs)

    def start(self):
        self.scheduler.start()
