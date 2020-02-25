from django.db import models

from utils.base_model import BaseModel

# from user.models import Users
# 五日资金流的行业名称 与字段对应名称
DB_N = {
    '房地产': 'realty',
    '机械行业': 'mechanical',
    '电子元件': 'ele_comp',
    '化工行业': 'chemical',
    '医药制造': 'medicine',
    '电子信息': 'ele_info',
    '输配电气': 'electrical',
    '农牧饲渔': 'farm',
    '工程建设': 'project',
    '有色金属': 'nonferrous',
    '材料行业': 'material',
    '汽车行业': 'car',
    '电力行业': 'ele_power',
    '券商信托': 'sec_trader',
    '通讯行业': 'communication',
    '文化传媒': 'culture',
    '商业百货': 'business',
    '软件服务': 'software',
    '交运设备': 'traffic',
    '纺织服装': 'spin',
    '塑胶制品': 'plastic',
    '银行': 'bank',
    '食品饮料': 'food',
    '石油行业': 'oil',
    '钢铁行业': 'steel',
    '造纸印刷': 'paper',
    '公用事业': 'public',
    '综合行业': 'comprehensive',
    '木业家具': 'wood',
    '水泥建材': 'build_material',
    '煤炭采选': 'coal',
    '金属制品': 'metal_product',
    '船舶制造': 'shipbuilding',
    '仪器仪表': 'instrument',
    '航天航空': 'aviation',
    '交运物流': 'logistics',
    '玻璃陶瓷': 'glass',
    '多元金融': 'diver_financial',
    '环保工程': 'env_pro',
    '国际贸易': 'world_trade',
    '酿酒行业': 'wine',
    '家电行业': 'household',
    '安防设备': 'sec_equip',
    '园林工程': 'garden',
    '港口水运': 'port',
    '农药兽药': 'pesticide',
    '包装材料': 'wrapper',
    '化纤行业': 'fiber',
    '化肥行业': 'fertilizer',
    '文教休闲': 'education',
    '医疗行业': 'medical_treat',
    '旅游酒店': 'travel',
    '民航机场': 'airport',
    '保险': 'insurance',
    '电信运营': 'tel_business',
    '珠宝首饰': 'jewelry',
    '高速公路': 'highway',
    '工艺商品': 'art_goods',
    '装修装饰': 'decoration',
    '贵金属': 'noble_metal',
    '专用设备': 'spec_equip',
    '每周和': 'week_sub',
    '上海周': 'week_sh',
    '深圳周': 'week_sz',
    '上深周': 'week_h_z',
    '资金流出比例': 'money_out_rate',
}


class A_stocks(models.Model):
    __tablename__ = 'a_stocks'
    # 表的结构:
    # id = models.IntegerField(primary_key=True)
    #  000001.SH
    ts_code = models.CharField(max_length=16, verbose_name='TS代码')
    #  000001
    symbol = models.CharField(max_length=10, unique=True, verbose_name='股票代码')
    name = models.CharField(max_length=16, verbose_name='股票名称')
    area = models.CharField(max_length=16, null=True, verbose_name='所在地域')
    industry = models.CharField(max_length=16, null=True, verbose_name='一级行业')
    industry_2 = models.CharField(max_length=16, null=True, verbose_name='二级行业')
    industry_3 = models.CharField(max_length=16, null=True, verbose_name='三级行业')
    fullname = models.CharField(max_length=128, null=True, verbose_name='股票全称')
    enname = models.CharField(max_length=128, null=True, verbose_name='英文全称')
    market = models.CharField(max_length=16, null=True, verbose_name='市场类型 （主板/中小板/创业板）')
    exchange = models.CharField(max_length=16, null=True, verbose_name='交易所代码')
    curr_type = models.CharField(max_length=16, null=True, verbose_name='交易货币')
    list_status = models.CharField(max_length=16, null=True, verbose_name='上市状态： L上市 D退市 P暂停上市')
    list_date = models.CharField(max_length=16, null=True, verbose_name='上市日期')
    # delist_date=models.CharField(max_length=16,verbose_name='退市日期')
    is_hs = models.CharField(max_length=16, null=True, verbose_name='是否沪深港通标的，N否 H沪股通 S深股通')

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = 'A股股票'
        verbose_name_plural = verbose_name


class UserStocks(BaseModel):
    user = models.ForeignKey(to='login.Users', verbose_name='用户', on_delete=models.CASCADE)
    stock = models.ForeignKey(to='A_stocks', related_name='mystocks', on_delete=models.CASCADE)
    stock_code = models.CharField(max_length=16, verbose_name='股票代码')

    class Meta:
        verbose_name = "用户股票管理"
        verbose_name_plural = verbose_name


class Money_out(BaseModel):
    __tablename__ = 'money_out'
    # id = Column(Integer, primary_key=True)
    c_time = models.DateField(unique=True,verbose_name='数据日期')
    # d_time=Column(DateTime,default=datetime.datetime.now)
    realty = models.FloatField(verbose_name="房地产")
    mechanical = models.FloatField(verbose_name="机械行业")
    ele_comp = models.FloatField(verbose_name="电子元件")
    chemical = models.FloatField(verbose_name="化工行业")
    medicine = models.FloatField(verbose_name="医药制造")
    ele_info = models.FloatField(verbose_name="电子信息")
    electrical = models.FloatField(verbose_name="输配电气")
    farm = models.FloatField(verbose_name="农牧饲渔")
    project = models.FloatField(verbose_name="工程建设")
    nonferrous = models.FloatField(verbose_name="有色金属")
    material = models.FloatField(verbose_name="材料行业")
    car = models.FloatField(verbose_name="汽车行业")
    ele_power = models.FloatField(verbose_name="电力行业")
    sec_trader = models.FloatField(verbose_name="券商信托")
    communication = models.FloatField(verbose_name="通讯行业")
    culture = models.FloatField(verbose_name="文化传媒")
    business = models.FloatField(verbose_name="商业百货")
    software = models.FloatField(verbose_name="软件服务")
    traffic = models.FloatField(verbose_name="交运设备")
    spin = models.FloatField(verbose_name="纺织服装")
    plastic = models.FloatField(verbose_name="塑胶制品")
    bank = models.FloatField(verbose_name="银行")
    food = models.FloatField(verbose_name="食品饮料")
    oil = models.FloatField(verbose_name="石油行业")
    steel = models.FloatField(verbose_name="钢铁行业")
    paper = models.FloatField(verbose_name="造纸印刷")
    public = models.FloatField(verbose_name="公用事业")
    comprehensive = models.FloatField(verbose_name="综合行业")
    wood = models.FloatField(verbose_name="木业家具")
    build_material = models.FloatField(verbose_name="水泥建材")
    coal = models.FloatField(verbose_name="煤炭采选")
    metal_product = models.FloatField(verbose_name="金属制品")
    shipbuilding = models.FloatField(verbose_name="船舶制造")
    instrument = models.FloatField(verbose_name="仪器仪表")
    aviation = models.FloatField(verbose_name="航天航空")
    logistics = models.FloatField(verbose_name="交运物流")
    glass = models.FloatField(verbose_name="玻璃陶瓷")
    diver_financial = models.FloatField(verbose_name="多元金融")
    env_pro = models.FloatField(verbose_name="环保工程")
    world_trade = models.FloatField(verbose_name="国际贸易")
    wine = models.FloatField(verbose_name="酿酒行业")
    household = models.FloatField(verbose_name="家电行业")
    sec_equip = models.FloatField(verbose_name="安防设备")
    garden = models.FloatField(verbose_name="园林工程")
    port = models.FloatField(verbose_name="港口水运")
    pesticide = models.FloatField(verbose_name="农药兽药")
    wrapper = models.FloatField(verbose_name="包装材料")
    fiber = models.FloatField(verbose_name="化纤行业")
    fertilizer = models.FloatField(verbose_name="化肥行业")
    education = models.FloatField(verbose_name="文教休闲")
    medical_treat = models.FloatField(verbose_name="医疗行业")
    travel = models.FloatField(verbose_name="旅游酒店")
    airport = models.FloatField(verbose_name="民航机场")
    insurance = models.FloatField(verbose_name="保险")
    tel_business = models.FloatField(verbose_name="电信运营")
    jewelry = models.FloatField(verbose_name="珠宝首饰")
    highway = models.FloatField(verbose_name="高速公路")
    art_goods = models.FloatField(verbose_name="工艺商品")
    decoration = models.FloatField(verbose_name="装修装饰")
    noble_metal = models.FloatField(verbose_name="贵金属")
    spec_equip = models.FloatField(verbose_name="专用设备")
    week_sub = models.FloatField(verbose_name="每周和")
    week_sh = models.FloatField(verbose_name="上海周")
    week_sz = models.FloatField(verbose_name="深圳周")
    week_h_z = models.FloatField(verbose_name="上深周")
    money_out_rate = models.FloatField(verbose_name="资金流出比例")


class WeekCompany(BaseModel):
    __tablename__ = 'week_company'
    c_time = models.DateField(unique=True,verbose_name='数据日期')
    # d_time=Column(DateTime,default=datetime.datetime.now)
    realty = models.CharField(max_length=16, verbose_name="房地产")
    mechanical = models.CharField(max_length=16, verbose_name="机械行业")
    ele_comp = models.CharField(max_length=16, verbose_name="电子元件")
    chemical = models.CharField(max_length=16, verbose_name="化工行业")
    medicine = models.CharField(max_length=16, verbose_name="医药制造")
    ele_info = models.CharField(max_length=16, verbose_name="电子信息")
    electrical = models.CharField(max_length=16, verbose_name="输配电气")
    farm = models.CharField(max_length=16, verbose_name="农牧饲渔")
    project = models.CharField(max_length=16, verbose_name="工程建设")
    nonferrous = models.CharField(max_length=16, verbose_name="有色金属")
    material = models.CharField(max_length=16, verbose_name="材料行业")
    car = models.CharField(max_length=16, verbose_name="汽车行业")
    ele_power = models.CharField(max_length=16, verbose_name="电力行业")
    sec_trader = models.CharField(max_length=16, verbose_name="券商信托")
    communication = models.CharField(max_length=16, verbose_name="通讯行业")
    culture = models.CharField(max_length=16, verbose_name="文化传媒")
    business = models.CharField(max_length=16, verbose_name="商业百货")
    software = models.CharField(max_length=16, verbose_name="软件服务")
    traffic = models.CharField(max_length=16, verbose_name="交运设备")
    spin = models.CharField(max_length=16, verbose_name="纺织服装")
    plastic = models.CharField(max_length=16, verbose_name="塑胶制品")
    bank = models.CharField(max_length=16, verbose_name="银行")
    food = models.CharField(max_length=16, verbose_name="食品饮料")
    oil = models.CharField(max_length=16, verbose_name="石油行业")
    steel = models.CharField(max_length=16, verbose_name="钢铁行业")
    paper = models.CharField(max_length=16, verbose_name="造纸印刷")
    public = models.CharField(max_length=16, verbose_name="公用事业")
    comprehensive = models.CharField(max_length=16, verbose_name="综合行业")
    wood = models.CharField(max_length=16, verbose_name="木业家具")
    build_material = models.CharField(max_length=16, verbose_name="水泥建材")
    coal = models.CharField(max_length=16, verbose_name="煤炭采选")
    metal_product = models.CharField(max_length=16, verbose_name="金属制品")
    shipbuilding = models.CharField(max_length=16, verbose_name="船舶制造")
    instrument = models.CharField(max_length=16, verbose_name="仪器仪表")
    aviation = models.CharField(max_length=16, verbose_name="航天航空")
    logistics = models.CharField(max_length=16, verbose_name="交运物流")
    glass = models.CharField(max_length=16, verbose_name="玻璃陶瓷")
    diver_financial = models.CharField(max_length=16, verbose_name="多元金融")
    env_pro = models.CharField(max_length=16, verbose_name="环保工程")
    world_trade = models.CharField(max_length=16, verbose_name="国际贸易")
    wine = models.CharField(max_length=16, verbose_name="酿酒行业")
    household = models.CharField(max_length=16, verbose_name="家电行业")
    sec_equip = models.CharField(max_length=16, verbose_name="安防设备")
    garden = models.CharField(max_length=16, verbose_name="园林工程")
    port = models.CharField(max_length=16, verbose_name="港口水运")
    pesticide = models.CharField(max_length=16, verbose_name="农药兽药")
    wrapper = models.CharField(max_length=16, verbose_name="包装材料")
    fiber = models.CharField(max_length=16, verbose_name="化纤行业")
    fertilizer = models.CharField(max_length=16, verbose_name="化肥行业")
    education = models.CharField(max_length=16, verbose_name="文教休闲")
    medical_treat = models.CharField(max_length=16, verbose_name="医疗行业")
    travel = models.CharField(max_length=16, verbose_name="旅游酒店")
    airport = models.CharField(max_length=16, verbose_name="民航机场")
    insurance = models.CharField(max_length=16, verbose_name="保险")
    tel_business = models.CharField(max_length=16, verbose_name="电信运营")
    jewelry = models.CharField(max_length=16, verbose_name="珠宝首饰")
    highway = models.CharField(max_length=16, verbose_name="高速公路")
    art_goods = models.CharField(max_length=16, verbose_name="工艺商品")
    decoration = models.CharField(max_length=16, verbose_name="装修装饰")
    noble_metal = models.CharField(max_length=16, verbose_name="贵金属")
    spec_equip = models.CharField(max_length=16, verbose_name="专用设备")


class FigureCheck(BaseModel):
    """技术指标复盘 诊断"""
    # stock=models.ForeignKey(to='A_stocks', related_name='myfigure', on_delete=models.CASCADE)
    month_boll_up = models.FloatField( verbose_name='月线boll上轨')
    month_boll_low = models.FloatField( verbose_name='月线boll下轨')
    month_deviation = models.CharField(max_length=16, verbose_name='月线MACD背离')

    week_boll_up = models.FloatField( verbose_name='周线boll上轨')
    week_boll_low = models.FloatField( verbose_name='周线boll下轨')
    week_boll_sd = models.CharField(max_length=16, verbose_name='周boll发散')
    week_d = models.FloatField( verbose_name='周线KDJ的D值')
    week_k = models.FloatField( verbose_name='周线KDJ的K值')
    week_deviation = models.CharField(max_length=16, verbose_name='周线MACD背离')
    week_macd_trend = models.CharField(max_length=16, verbose_name='周线MACD趋势')
    week_ma_trend = models.CharField(max_length=16, verbose_name='周线MA20趋势')
    week_swing_vol = models.CharField(max_length=16, verbose_name='周线量价异常')
    week_ma_20 = models.FloatField( verbose_name='周20均线值')

    day_boll_up = models.FloatField( verbose_name='日线boll下轨')
    day_boll_low = models.FloatField( verbose_name='日线boll下轨')
    day_boll_sd = models.CharField(max_length=16, verbose_name='日boll发散')
    day_d = models.FloatField( verbose_name='日线KDJ的D值')
    day_k = models.FloatField( verbose_name='日线KDJ的K值')
    day_deviation = models.CharField(max_length=16, verbose_name='日线MACD背离')
    day_macd_trend = models.CharField(max_length=16, verbose_name='日线MACD趋势')
    day_ma_trend = models.CharField(max_length=16, verbose_name='日线MA20趋势')
    day_ma_20 = models.FloatField( verbose_name='日20均线值')
    day_swing_vol = models.CharField(max_length=16, verbose_name='日线量价异常')

    now_price = models.FloatField( verbose_name='现价')


class FinanceCheck(BaseModel):
    """财务指标诊断"""

    pass


class RzRq(BaseModel):
    trade_date = models.DateField(verbose_name='数据日期')
    stock = models.ForeignKey(to='A_stocks', related_name='rzrq', on_delete=models.CASCADE)
    zdf = models.FloatField(verbose_name="涨跌幅%")
    spj = models.FloatField(verbose_name="收盘价")
    rqpjcb = models.FloatField(verbose_name="融券平均成本")

    rzmre = models.FloatField( verbose_name="融资买入额(亿)")
    rzche = models.FloatField( verbose_name="融资偿还额(亿)")
    rzjme = models.FloatField( verbose_name="融资净买入(亿)")
    rzye = models.FloatField( verbose_name="融资余额(亿)")

    rzrqye = models.FloatField( verbose_name="融资融券余额(亿)")
    rzrqyecz = models.FloatField( verbose_name="融资融券余额差值(亿)")
    rzyezb = models.FloatField(verbose_name="余额占流通市值比%")

    rqmcl = models.IntegerField(verbose_name="融券卖出量(股)")
    rqchl = models.IntegerField(verbose_name="融券偿还量(股)")
    rqjmg = models.IntegerField(verbose_name="融券净卖(股)")
    rqyl = models.IntegerField(verbose_name="融券余量(股)")
    rqye = models.FloatField(verbose_name="融券余额(元)")

    class Meta:
        verbose_name = "融资融券表"
        verbose_name_plural = verbose_name

# todo 将trade_date改为日期型
class TuShareRzRq(BaseModel):
    trade_date = models.DateField( verbose_name='交易日期')
    ts_code = models.CharField(max_length=16, verbose_name='股票代码')
    rzye = models.FloatField(verbose_name='融资余额(元)')
    rqye = models.FloatField(verbose_name='融券余额(元)')
    rzmre = models.FloatField(verbose_name='融资买入额(元)')
    rqyl = models.FloatField(verbose_name='融券余量(股, 份, 手)')
    rzche = models.FloatField(verbose_name='融资偿还额(元)')
    rqchl = models.FloatField(verbose_name='融券偿还量((股, 份, 手)')
    rqmcl = models.FloatField(verbose_name='融券卖出量((股, 份, 手)')
    rzrqye = models.FloatField(verbose_name='融资融券余额(元)')

    class Meta:
        verbose_name = "tushare融资融券"
        verbose_name_plural = verbose_name

#
# data = {
#     "date": '日期',
#     "scode": "601166",  # code
#     "spj": '收盘价',  #
#     "market": "融资融券_沪证",
#     "secname": "兴业银行",  # 名称
#     "zdf": '涨跌幅%',  #
#
#     "rzmre": '融资买入额(亿)',
#     "rzche": '融资偿还额(亿)',
#     "rzjme": '融资净买入(亿)',
#     "rzye": '融资余额(亿)',
#
#     "rqmcl": '融券卖出量(股)',
#     "rqchl": '融券偿还量(股)',
#     "rqjmg": '融券净卖(股)',
#     "rqyl": '融券余量(股)',
#     "rqye": '融券余额(元)',
#
#     "rzrqye": '融资融券余额(亿)',
#     "rzyezb": '余额占流通市值比%',
#     "rzrqyecz": '融资融券余额差值(亿)',
#
#     # "sz": 345228341928.120000,  #
#     # "kcb": 0,
#     "rqmcl3d": '融券卖出量3d',
#     "rzmre3d": '融资买入额3d',
#     "rqjmg3d": '融券净卖股3d',
#     "rqchl3d": '融券偿还量3d',
#     "rzche3d": '融资偿还额3d',
#     "rzjme3d": '融资净买额3d',
#     "rchange3dcp": '3日涨跌幅',
#
#     "rzmre5d": '融资买入额5d',
#     "rqmcl5d": '融券卖出量5d',
#     "rqjmg5d": '融券净卖股5d',
#     "rqchl5d": '融券偿还量5d',
#     "rzjme5d": '融资净买额5d',
#     "rzche5d": '融资偿还额5d',
#     "rchange5dcp": '5日涨跌幅',
#
#     "rqjmg10d": '融券净卖股10d',
#     "rzche10d": '融券偿还量10d',
#     "rqchl10d": '融券偿还量10d',
#     "rqmcl10d": '融券偿还量10d',
#     "rzjme10d": '融资净买额10d',
#     "rzmre10d": '融资买入额10d',
#     "rchange10dcp": '10日涨跌幅',
#
# }
#

# class FinanceData(BaseModel):
#
#
#     class Meta:
#         verbose_name = '个股财务数据'
#         verbose_name_plural = verbose_name


class FinanceQuota(BaseModel):
    ts_code = models.CharField(max_length=16,verbose_name='TS代码')
    ann_date = models.CharField(max_length=16,verbose_name='公告日期')
    end_date = models.CharField(max_length=16,verbose_name='报告期')
    eps = models.FloatField(null=True,verbose_name='基本每股收益')
    dt_eps = models.FloatField(null=True,verbose_name='稀释每股收益')
    total_revenue_ps = models.FloatField(null=True,verbose_name='每股营业总收入')
    revenue_ps = models.FloatField(null=True,verbose_name='每股营业收入')
    capital_rese_ps = models.FloatField(null=True,verbose_name='每股资本公积')
    surplus_rese_ps = models.FloatField(null=True,verbose_name='每股盈余公积')
    undist_profit_ps = models.FloatField(null=True,verbose_name='每股未分配利润')
    extra_item = models.FloatField(null=True,verbose_name='非经常性损益')
    profit_dedt = models.FloatField(null=True,verbose_name='扣除非经常性损益后的净利润')
    gross_margin = models.FloatField(null=True,verbose_name='毛利')
    current_ratio = models.FloatField(null=True,verbose_name='流动比率')
    quick_ratio = models.FloatField(null=True,verbose_name='速动比率')
    cash_ratio = models.FloatField(null=True,verbose_name='保守速动比率')
    ar_turn = models.FloatField(null=True,verbose_name='应收账款周转率')
    ca_turn = models.FloatField(null=True,verbose_name='流动资产周转率')
    fa_turn = models.FloatField(null=True,verbose_name='固定资产周转率')
    assets_turn = models.FloatField(null=True,verbose_name='总资产周转率')
    op_income = models.FloatField(null=True,verbose_name='经营活动净收益')
    ebit = models.FloatField(null=True,verbose_name='息税前利润')
    ebitda = models.FloatField(null=True,verbose_name='息税折旧摊销前利润')
    fcff = models.FloatField(null=True,verbose_name='企业自由现金流量')
    fcfe = models.FloatField(null=True,verbose_name='股权自由现金流量')
    current_exint = models.FloatField(null=True,verbose_name='无息流动负债')
    noncurrent_exint = models.FloatField(null=True,verbose_name='无息非流动负债')
    interestdebt = models.FloatField(null=True,verbose_name='带息债务')
    netdebt = models.FloatField(null=True,verbose_name='净债务')
    tangible_asset = models.FloatField(null=True,verbose_name='有形资产')
    working_capital = models.FloatField(null=True,verbose_name='营运资金')
    networking_capital = models.FloatField(null=True,verbose_name='营运流动资本')
    invest_capital = models.FloatField(null=True,verbose_name='全部投入资本')
    retained_earnings = models.FloatField(null=True,verbose_name='留存收益')
    diluted2_eps = models.FloatField(null=True,verbose_name='期末摊薄每股收益')
    bps = models.FloatField(null=True,verbose_name='每股净资产')
    ocfps = models.FloatField(null=True,verbose_name='每股经营活动产生的现金流量净额')
    retainedps = models.FloatField(null=True,verbose_name='每股留存收益')
    cfps = models.FloatField(null=True,verbose_name='每股现金流量净额')
    ebit_ps = models.FloatField(null=True,verbose_name='每股息税前利润')
    fcff_ps = models.FloatField(null=True,verbose_name='每股企业自由现金流量')
    fcfe_ps = models.FloatField(null=True,verbose_name='每股股东自由现金流量')
    netprofit_margin = models.FloatField(null=True,verbose_name='销售净利率')
    grossprofit_margin = models.FloatField(null=True,verbose_name='销售毛利率')
    cogs_of_sales = models.FloatField(null=True,verbose_name='销售成本率')
    expense_of_sales = models.FloatField(null=True,verbose_name='销售期间费用率')
    profit_to_gr = models.FloatField(null=True,verbose_name='净利润/营业总收入')
    saleexp_to_gr = models.FloatField(null=True,verbose_name='销售费用/营业总收入')
    adminexp_of_gr = models.FloatField(null=True,verbose_name='管理费用/营业总收入')
    finaexp_of_gr = models.FloatField(null=True,verbose_name='财务费用/营业总收入')
    impai_ttm = models.FloatField(null=True,verbose_name='资产减值损失/营业总收入')
    gc_of_gr = models.FloatField(null=True,verbose_name='营业总成本/营业总收入')
    op_of_gr = models.FloatField(null=True,verbose_name='营业利润/营业总收入')
    ebit_of_gr = models.FloatField(null=True,verbose_name='息税前利润/营业总收入')
    roe = models.FloatField(null=True,verbose_name='净资产收益率')
    roe_waa = models.FloatField(null=True,verbose_name='加权平均净资产收益率')
    roe_dt = models.FloatField(null=True,verbose_name='净资产收益率(扣除非经常损益)')
    roa = models.FloatField(null=True,verbose_name='总资产报酬率')
    npta = models.FloatField(null=True,verbose_name='总资产净利润')
    roic = models.FloatField(null=True,verbose_name='投入资本回报率')
    roe_yearly = models.FloatField(null=True,verbose_name='年化净资产收益率')
    roa2_yearly = models.FloatField(null=True,verbose_name='年化总资产报酬率')
    debt_to_assets = models.FloatField(null=True,verbose_name='资产负债率')
    assets_to_eqt = models.FloatField(null=True,verbose_name='权益乘数')
    dp_assets_to_eqt = models.FloatField(null=True,verbose_name='权益乘数(杜邦分析)')
    ca_to_assets = models.FloatField(null=True,verbose_name='流动资产/总资产')
    nca_to_assets = models.FloatField(null=True,verbose_name='非流动资产/总资产')
    tbassets_to_totalassets = models.FloatField(null=True,verbose_name='有形资产/总资产')
    int_to_talcap = models.FloatField(null=True,verbose_name='带息债务/全部投入资本')
    eqt_to_talcapital = models.FloatField(null=True,verbose_name='归属于母公司的股东权益/全部投入资本')
    currentdebt_to_debt = models.FloatField(null=True,verbose_name='流动负债/负债合计')
    longdeb_to_debt = models.FloatField(null=True,verbose_name='非流动负债/负债合计')
    ocf_to_shortdebt = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/流动负债')
    debt_to_eqt = models.FloatField(null=True,verbose_name='产权比率')
    eqt_to_debt = models.FloatField(null=True,verbose_name='归属于母公司的股东权益/负债合计')
    eqt_to_interestdebt = models.FloatField(null=True,verbose_name='归属于母公司的股东权益/带息债务')
    tangibleasset_to_debt = models.FloatField(null=True,verbose_name='有形资产/负债合计')
    tangasset_to_intdebt = models.FloatField(null=True,verbose_name='有形资产/带息债务')
    tangibleasset_to_netdebt = models.FloatField(null=True,verbose_name='有形资产/净债务')
    ocf_to_debt = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/负债合计')
    turn_days = models.FloatField(null=True,verbose_name='营业周期')
    roa_yearly = models.FloatField(null=True,verbose_name='年化总资产净利率')
    roa_dp = models.FloatField(null=True,verbose_name='总资产净利率(杜邦分析)')
    fixed_assets = models.FloatField(null=True,verbose_name='固定资产合计')
    profit_to_op = models.FloatField(null=True,verbose_name='利润总额／营业收入')
    q_saleexp_to_gr = models.FloatField(null=True,verbose_name='销售费用／营业总收入 (单季度)')
    q_gc_to_gr = models.FloatField(null=True,verbose_name='营业总成本／营业总收入 (单季度)')
    q_roe = models.FloatField(null=True,verbose_name='净资产收益率(单季度)')
    q_dt_roe = models.FloatField(null=True,verbose_name='净资产单季度收益率(扣除非经常损益)')
    q_npta = models.FloatField(null=True,verbose_name='总资产净利润(单季度)')
    q_ocf_to_sales = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额／营业收入(单季度)')
    basic_eps_yoy = models.FloatField(null=True,verbose_name='基本每股收益同比增长率(%)')
    dt_eps_yoy = models.FloatField(null=True,verbose_name='稀释每股收益同比增长率(%)')
    cfps_yoy = models.FloatField(null=True,verbose_name='每股经营活动产生的现金流量净额同比增长率(%)')
    op_yoy = models.FloatField(null=True,verbose_name='营业利润同比增长率(%)')
    ebt_yoy = models.FloatField(null=True,verbose_name='利润总额同比增长率(%)')
    netprofit_yoy = models.FloatField(null=True,verbose_name='归属母公司股东的净利润同比增长率(%)')
    dt_netprofit_yoy = models.FloatField(null=True,verbose_name='归属母公司股东的净利润-扣除非经常损益同比增长率(%)')
    ocf_yoy = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额同比增长率(%)')
    roe_yoy = models.FloatField(null=True,verbose_name='净资产收益率(摊薄)同比增长率(%)')
    bps_yoy = models.FloatField(null=True,verbose_name='每股净资产相对年初增长率(%)')
    assets_yoy = models.FloatField(null=True,verbose_name='资产总计相对年初增长率(%)')
    eqt_yoy = models.FloatField(null=True,verbose_name='归属母公司的股东权益相对年初增长率(%)')
    tr_yoy = models.FloatField(null=True,verbose_name='营业总收入同比增长率(%)')
    or_yoy = models.FloatField(null=True,verbose_name='营业收入同比增长率(%)')
    q_sales_yoy = models.FloatField(null=True,verbose_name='营业收入同比增长率(%)(单季度)')
    q_op_qoq = models.FloatField(null=True,verbose_name='营业利润环比增长率(%)(单季度)')
    equity_yoy = models.FloatField(null=True,verbose_name='净资产同比增长率')
    # 未开放的数据
    invturn_days = models.FloatField(null=True,verbose_name='存货周转天数')
    arturn_days = models.FloatField(null=True,verbose_name='应收账款周转天数')
    inv_turn = models.FloatField(null=True,verbose_name='存货周转率')
    valuechange_income = models.FloatField(null=True,verbose_name='价值变动净收益')
    interst_income = models.FloatField(null=True,verbose_name='利息费用')
    daa = models.FloatField(null=True,verbose_name='折旧与摊销')
    roe_avg = models.FloatField(null=True,verbose_name='平均净资产收益率(null=True,增发条件)')
    opincome_of_ebt = models.FloatField(null=True,verbose_name='经营活动净收益/利润总额')
    investincome_of_ebt = models.FloatField(null=True,verbose_name='价值变动净收益/利润总额')
    n_op_profit_of_ebt = models.FloatField(null=True,verbose_name='营业外收支净额/利润总额')
    tax_to_ebt = models.FloatField(null=True,verbose_name='所得税/利润总额')
    dtprofit_to_profit = models.FloatField(null=True,verbose_name='扣除非经常损益后的净利润/净利润')
    salescash_to_or = models.FloatField(null=True,verbose_name='销售商品提供劳务收到的现金/营业收入')
    ocf_to_or = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/营业收入')
    ocf_to_opincome = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/经营活动净收益')
    capitalized_to_da = models.FloatField(null=True,verbose_name='资本支出/折旧和摊销')
    ocf_to_interestdebt = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/带息债务')
    ocf_to_netdebt = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额/净债务')
    ebit_to_interest = models.FloatField(null=True,verbose_name='已获利息倍数(null=True,EBIT/利息费用)')
    longdebt_to_workingcapital = models.FloatField(null=True,verbose_name='长期债务与营运资金比率')
    ebitda_to_debt = models.FloatField(null=True,verbose_name='息税折旧摊销前利润/负债合计')
    profit_prefin_exp = models.FloatField(null=True,verbose_name='扣除财务费用前营业利润')
    non_op_profit = models.FloatField(null=True,verbose_name='非营业利润')
    op_to_ebt = models.FloatField(null=True,verbose_name='营业利润／利润总额')
    nop_to_ebt = models.FloatField(null=True,verbose_name='非营业利润／利润总额')
    ocf_to_profit = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额／营业利润')
    cash_to_liqdebt = models.FloatField(null=True,verbose_name='货币资金／流动负债')
    cash_to_liqdebt_withinterest = models.FloatField(null=True,verbose_name='货币资金／带息流动负债')
    op_to_liqdebt = models.FloatField(null=True,verbose_name='营业利润／流动负债')
    op_to_debt = models.FloatField(null=True,verbose_name='营业利润／负债合计')
    roic_yearly = models.FloatField(null=True,verbose_name='年化投入资本回报率')
    total_fa_trun = models.FloatField(null=True,verbose_name='固定资产合计周转率')
    q_opincome = models.FloatField(null=True,verbose_name='经营活动单季度净收益')
    q_investincome = models.FloatField(null=True,verbose_name='价值变动单季度净收益')
    q_dtprofit = models.FloatField(null=True,verbose_name='扣除非经常损益后的单季度净利润')
    q_eps = models.FloatField(null=True,verbose_name='每股收益(单季度)')
    q_netprofit_margin = models.FloatField(null=True,verbose_name='销售净利率(单季度)')
    q_gsprofit_margin = models.FloatField(null=True,verbose_name='销售毛利率(单季度)')
    q_exp_to_sales = models.FloatField(null=True,verbose_name='销售期间费用率(单季度)')
    q_profit_to_gr = models.FloatField(null=True,verbose_name='净利润／营业总收入(单季度)')
    q_adminexp_to_gr = models.FloatField(null=True,verbose_name='管理费用／营业总收入 (单季度)')
    q_finaexp_to_gr = models.FloatField(null=True,verbose_name='财务费用／营业总收入 (单季度)')
    q_impair_to_gr_ttm = models.FloatField(null=True,verbose_name='资产减值损失／营业总收入(单季度)')
    q_op_to_gr = models.FloatField(null=True,verbose_name='营业利润／营业总收入(单季度)')
    q_opincome_to_ebt = models.FloatField(null=True,verbose_name='经营活动净收益／利润总额(单季度)')
    q_investincome_to_ebt = models.FloatField(null=True,verbose_name='价值变动净收益／利润总额(单季度)')
    q_dtprofit_to_profit = models.FloatField(null=True,verbose_name='扣除非经常损益后的净利润／净利润(单季度)')
    q_salescash_to_or = models.FloatField(null=True,verbose_name='销售商品提供劳务收到的现金／营业收入(单季度)')
    q_ocf_to_or = models.FloatField(null=True,verbose_name='经营活动产生的现金流量净额／经营活动净收益(单季度)')
    q_gr_yoy = models.FloatField(null=True,verbose_name='营业总收入同比增长率(%)(单季度)')
    q_gr_qoq = models.FloatField(null=True,verbose_name='营业总收入环比增长率(%)(单季度)')
    q_sales_qoq = models.FloatField(null=True,verbose_name='营业收入环比增长率(%)(单季度)')
    q_op_yoy = models.FloatField(null=True,verbose_name='营业利润同比增长率(%)(单季度)')
    q_profit_yoy = models.FloatField(null=True,verbose_name='净利润同比增长率(%)(单季度)')
    q_profit_qoq = models.FloatField(null=True,verbose_name='净利润环比增长率(%)(单季度)')
    q_netprofit_yoy = models.FloatField(null=True,verbose_name='归属母公司股东的净利润同比增长率(%)(单季度)')
    q_netprofit_qoq = models.FloatField(null=True,verbose_name='归属母公司股东的净利润环比增长率(%)(单季度)')
    rd_exp = models.FloatField(null=True,verbose_name='研发费用')
    # update_flag = models.CharField(max_length=16,verbose_name='更新标识')
    hash=models.CharField(unique=True,max_length=32,verbose_name='MD5值')
    class Meta:
        verbose_name = '个股财务指标数据'
        verbose_name_plural = verbose_name

class MarketDayQuota(BaseModel):
    trade_date = models.DateField(unique=True,verbose_name='数据日期')
    total_mv=models.FloatField(verbose_name='市场总市值')
    float_mv=models.FloatField(verbose_name='市场流通市值')
    day_mid_amount=models.FloatField(verbose_name='市场成交额中位数')
    day_mid_pe=models.FloatField(verbose_name='市场PE中位数')
    day_mid_pe_ttm=models.FloatField(verbose_name='市场PE-TTM 中位数')
    day_mid_pb=models.FloatField(verbose_name='市场PB中位数')
    day_low_10=models.IntegerField(null=True,verbose_name='市场跌停数量')
    day_up_10=models.IntegerField(null=True,verbose_name='市场涨停数量')
    sh_rzrqye=models.FloatField(null=True,verbose_name='上海融资融券余额')
    sh_rzmre=models.FloatField(null=True,verbose_name='上海融资买入额')
    sh_rqye=models.FloatField(null=True,verbose_name='上海融券余额')
    sz_rzrqye=models.FloatField(null=True,verbose_name='深圳融资融券余额')
    sz_rzmre = models.FloatField(null=True, verbose_name='深圳融资买入额')
    sz_rqye = models.FloatField(null=True, verbose_name='深圳融券余额')
    turnover_rate_f=models.FloatField(null=True,verbose_name='基于自由流通市值的换手率')
    turnover_rate=models.FloatField(null=True,verbose_name='换手率')
    pb_lt_1=models.IntegerField(null=True,verbose_name='破净股个数')
    class Meta:
        verbose_name = '市场每日指标数据'
        verbose_name_plural = verbose_name

# 市场每日交易数据表
class TradeData(BaseModel):
    stock = models.ForeignKey(to='A_stocks', related_name='mytradedata', on_delete=models.CASCADE)
    ts_code = models.CharField(max_length=16,verbose_name='股票代码')
    trade_date = models.DateField(verbose_name='交易日期')
    open = models.FloatField(verbose_name='开盘价')
    high = models.FloatField(verbose_name='最高价')
    low = models.FloatField(verbose_name='最低价')
    close = models.FloatField(verbose_name='收盘价')
    pre_close = models.FloatField(verbose_name='昨收价')
    change = models.FloatField(verbose_name='涨跌额')
    pct_chg = models.FloatField(verbose_name='涨跌幅 （未复权，如果是复权请用 ')
    vol = models.FloatField(verbose_name='成交量 （手）')
    amount = models.FloatField(verbose_name='成交额 （千元）')

    class Meta:
        verbose_name = '市场每日交易数据'
        verbose_name_plural = verbose_name


class PE15Boll(BaseModel):
    stock=models.ForeignKey(A_stocks,related_name='stocks',on_delete=models.CASCADE)
    last_year_pe=models.IntegerField(verbose_name='静态PE')
    now_pe=models.IntegerField(verbose_name='动态PE')
    week_boll_low=models.FloatField(verbose_name='周线Boll下轨')
    week_boll_up=models.FloatField(verbose_name='周线Boll下轨')


class MonthCapitalSettlement(BaseModel):
    # 中国证券登记结算数据源 的每月结算数据
    trade_date = models.DateField(verbose_name='交易月份')
    sh_money_total=models.FloatField(verbose_name='上海结算资金总额(亿)')
    sh_money_net=models.FloatField(verbose_name='上海结算资金净额(亿)')
    sz_money_total=models.FloatField(verbose_name='深圳结算资金总额(亿)')
    sz_money_net=models.FloatField(verbose_name='深圳结算资金净额(亿)')
    us_money_total=models.FloatField(verbose_name='美元结算资金总额(亿)')
    us_money_net=models.FloatField(verbose_name='美元结算资金净额(亿)')
    hk_money_total=models.FloatField(verbose_name='港元结算资金总额(亿)')
    hk_money_net=models.FloatField(verbose_name='港元结算资金净额(亿)')