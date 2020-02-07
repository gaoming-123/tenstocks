# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:39
# Editor : gmj
# Desc   :
from redis import StrictRedis

from config import REDIS_CONFIG


class RedisClient(object):
    def __init__(self, my_config=REDIS_CONFIG):
        self.config = my_config
        self.cli = self.connect()
        self.stock_key=self.config['STOCK_KEY']
        self.index_key=self.config['INDEX_KEY']
    def connect(self):
        return StrictRedis(host=self.config['HOST'],
                           port=self.config['PORT'],
                            password=self.config.get('PWD'),
                           db=self.config['DB'], )

    def add_stock(self, value):
        self.cli.lpush(self.stock_key,value)

    def add_index(self,value):
        self.cli.lpush(self.index_key,value)

    def read_stocks(self):
        return self.cli.lrange(self.stock_key,0,self.cli.llen(self.stock_key))

    def read_index(self):
        return self.cli.lrange(self.index_key,0,self.cli.llen(self.index_key))


redis_cli=RedisClient()

if __name__ == '__main__':
    from config import INDEX_S,MY_STOCKS
    for k,v in MY_STOCKS.items():
        redis_cli.add_stock(f'{k}:{v}')
    for k,v in INDEX_S.items():
        redis_cli.add_index(f'{k}:{v}')