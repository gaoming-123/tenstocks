# encoding: utf-8
# author:  gao-ming
# time:  2019/7/14--21:33
# desc:

# 是tushare的用户token
MY_TOKEN = '4516ff6d7ad8bd6c3393fc750c46fb2eed9f0ee3996ecc8f656943a1'
# 要监测的个股列表

# 目标邮箱地址
DESTINATION_EMAIL=['451574449@qq.com']

# redisÅäÖÃ
REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': 6379,
    'PWD': 'gmj760808',
    'DB': 15,
    # 'SET_KEY': '',
    'STOCK_KEY': 'stocks',
    'INDEX_KEY': 'indexs',

}
ll=[]
for k,v in MY_STOCKS.items():
    ll.append(f'{k}:{v}')

