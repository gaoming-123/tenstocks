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
    ts_code=models.CharField(max_length=16,verbose_name='TS代码')
    #  000001
    symbol=models.CharField(max_length=10,unique=True,verbose_name='股票代码')
    name=models.CharField(max_length=16,verbose_name='股票名称')
    area=models.CharField(max_length=16,verbose_name='所在地域')
    industry=models.CharField(max_length=16,verbose_name='一级行业')
    industry_2=models.CharField(max_length=16,verbose_name='二级行业')
    industry_3=models.CharField(max_length=16,verbose_name='三级行业')
    fullname=models.CharField(max_length=16,verbose_name='股票全称')
    enname=models.CharField(max_length=16,verbose_name='英文全称')
    market=models.CharField(max_length=16,verbose_name='市场类型 （主板/中小板/创业板）')
    exchange=models.CharField(max_length=16,verbose_name='交易所代码')
    curr_type=models.CharField(max_length=16,verbose_name='交易货币')
    list_status=models.CharField(max_length=16,verbose_name='上市状态： L上市 D退市 P暂停上市')
    list_date=models.CharField(max_length=16,verbose_name='上市日期')
    # delist_date=models.CharField(max_length=16,verbose_name='退市日期')
    is_hs=models.CharField(max_length=16,verbose_name='是否沪深港通标的，N否 H沪股通 S深股通')

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name='A股股票'
        verbose_name_plural = verbose_name


class UserStocks(BaseModel):
    user=models.ForeignKey(to='user.Users',verbose_name='用户',on_delete=models.CASCADE )
    stock=models.ForeignKey(to='A_stocks',related_name='股票',on_delete=models.CASCADE )
    stock_code=models.CharField(max_length=16,verbose_name='股票代码')
    class Meta:
        verbose_name = "用户股票管理"
        verbose_name_plural = verbose_name


class Money_out(BaseModel):
    __tablename__ = 'money_out'
    # id = Column(Integer, primary_key=True)
    c_time = models.DateField(verbose_name='数据日期')
    # d_time=Column(DateTime,default=datetime.datetime.now)
    realty = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="房地产")
    mechanical = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="机械行业")
    ele_comp = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="电子元件")
    chemical = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="化工行业")
    medicine = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="医药制造")
    ele_info = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="电子信息")
    electrical = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="输配电气")
    farm = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="农牧饲渔")
    project = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="工程建设")
    nonferrous = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="有色金属")
    material = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="材料行业")
    car = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="汽车行业")
    ele_power = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="电力行业")
    sec_trader = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="券商信托")
    communication = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="通讯行业")
    culture = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="文化传媒")
    business = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="商业百货")
    software = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="软件服务")
    traffic = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="交运设备")
    spin = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="纺织服装")
    plastic = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="塑胶制品")
    bank = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="银行")
    food = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="食品饮料")
    oil = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="石油行业")
    steel = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="钢铁行业")
    paper = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="造纸印刷")
    public = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="公用事业")
    comprehensive = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="综合行业")
    wood = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="木业家具")
    build_material = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="水泥建材")
    coal = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="煤炭采选")
    metal_product = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="金属制品")
    shipbuilding = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="船舶制造")
    instrument = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="仪器仪表")
    aviation = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="航天航空")
    logistics = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="交运物流")
    glass = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="玻璃陶瓷")
    diver_financial = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="多元金融")
    env_pro = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="环保工程")
    world_trade = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="国际贸易")
    wine = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="酿酒行业")
    household = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="家电行业")
    sec_equip = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="安防设备")
    garden = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="园林工程")
    port = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="港口水运")
    pesticide = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="农药兽药")
    wrapper = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="包装材料")
    fiber = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="化纤行业")
    fertilizer = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="化肥行业")
    education = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="文教休闲")
    medical_treat = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="医疗行业")
    travel = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="旅游酒店")
    airport = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="民航机场")
    insurance = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="保险")
    tel_business = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="电信运营")
    jewelry = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="珠宝首饰")
    highway = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="高速公路")
    art_goods = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="工艺商品")
    decoration = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="装修装饰")
    noble_metal = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="贵金属")
    spec_equip = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="专用设备")
    week_sub = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="每周和")
    week_sh = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="上海周")
    week_sz = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="深圳周")
    week_h_z = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="上深周")
    money_out_rate = models.DecimalField(max_digits=9,decimal_places=3,verbose_name="资金流出比例")


class WeekCompany(BaseModel):
    __tablename__ = 'week_company'
    c_time = models.DateField(verbose_name='数据日期')
    # d_time=Column(DateTime,default=datetime.datetime.now)
    realty = models.CharField(max_length=16,verbose_name="房地产")
    mechanical = models.CharField(max_length=16,verbose_name="机械行业")
    ele_comp = models.CharField(max_length=16,verbose_name="电子元件")
    chemical = models.CharField(max_length=16,verbose_name="化工行业")
    medicine = models.CharField(max_length=16,verbose_name="医药制造")
    ele_info = models.CharField(max_length=16,verbose_name="电子信息")
    electrical = models.CharField(max_length=16,verbose_name="输配电气")
    farm = models.CharField(max_length=16,verbose_name="农牧饲渔")
    project = models.CharField(max_length=16,verbose_name="工程建设")
    nonferrous = models.CharField(max_length=16,verbose_name="有色金属")
    material = models.CharField(max_length=16,verbose_name="材料行业")
    car = models.CharField(max_length=16,verbose_name="汽车行业")
    ele_power = models.CharField(max_length=16,verbose_name="电力行业")
    sec_trader = models.CharField(max_length=16,verbose_name="券商信托")
    communication = models.CharField(max_length=16,verbose_name="通讯行业")
    culture = models.CharField(max_length=16,verbose_name="文化传媒")
    business = models.CharField(max_length=16,verbose_name="商业百货")
    software = models.CharField(max_length=16,verbose_name="软件服务")
    traffic = models.CharField(max_length=16,verbose_name="交运设备")
    spin = models.CharField(max_length=16,verbose_name="纺织服装")
    plastic = models.CharField(max_length=16,verbose_name="塑胶制品")
    bank = models.CharField(max_length=16,verbose_name="银行")
    food = models.CharField(max_length=16,verbose_name="食品饮料")
    oil = models.CharField(max_length=16,verbose_name="石油行业")
    steel = models.CharField(max_length=16,verbose_name="钢铁行业")
    paper = models.CharField(max_length=16,verbose_name="造纸印刷")
    public = models.CharField(max_length=16,verbose_name="公用事业")
    comprehensive = models.CharField(max_length=16,verbose_name="综合行业")
    wood = models.CharField(max_length=16,verbose_name="木业家具")
    build_material = models.CharField(max_length=16,verbose_name="水泥建材")
    coal = models.CharField(max_length=16,verbose_name="煤炭采选")
    metal_product = models.CharField(max_length=16,verbose_name="金属制品")
    shipbuilding = models.CharField(max_length=16,verbose_name="船舶制造")
    instrument = models.CharField(max_length=16,verbose_name="仪器仪表")
    aviation = models.CharField(max_length=16,verbose_name="航天航空")
    logistics = models.CharField(max_length=16,verbose_name="交运物流")
    glass = models.CharField(max_length=16,verbose_name="玻璃陶瓷")
    diver_financial = models.CharField(max_length=16,verbose_name="多元金融")
    env_pro = models.CharField(max_length=16,verbose_name="环保工程")
    world_trade = models.CharField(max_length=16,verbose_name="国际贸易")
    wine = models.CharField(max_length=16,verbose_name="酿酒行业")
    household = models.CharField(max_length=16,verbose_name="家电行业")
    sec_equip = models.CharField(max_length=16,verbose_name="安防设备")
    garden = models.CharField(max_length=16,verbose_name="园林工程")
    port = models.CharField(max_length=16,verbose_name="港口水运")
    pesticide = models.CharField(max_length=16,verbose_name="农药兽药")
    wrapper = models.CharField(max_length=16,verbose_name="包装材料")
    fiber = models.CharField(max_length=16,verbose_name="化纤行业")
    fertilizer = models.CharField(max_length=16,verbose_name="化肥行业")
    education = models.CharField(max_length=16,verbose_name="文教休闲")
    medical_treat = models.CharField(max_length=16,verbose_name="医疗行业")
    travel = models.CharField(max_length=16,verbose_name="旅游酒店")
    airport = models.CharField(max_length=16,verbose_name="民航机场")
    insurance = models.CharField(max_length=16,verbose_name="保险")
    tel_business = models.CharField(max_length=16,verbose_name="电信运营")
    jewelry = models.CharField(max_length=16,verbose_name="珠宝首饰")
    highway = models.CharField(max_length=16,verbose_name="高速公路")
    art_goods = models.CharField(max_length=16,verbose_name="工艺商品")
    decoration = models.CharField(max_length=16,verbose_name="装修装饰")
    noble_metal = models.CharField(max_length=16,verbose_name="贵金属")
    spec_equip = models.CharField(max_length=16,verbose_name="专用设备")


class FigureCheck(BaseModel):
    """技术指标复盘 诊断"""
    month_boll_up=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='月线boll上轨')
    month_boll_low=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='月线boll下轨')
    month_deviation=models.CharField(max_length=16,verbose_name='月线MACD背离')

    week_boll_up=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='周线boll上轨')
    week_boll_low=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='周线boll下轨')
    week_boll_sd=models.CharField(max_length=16,verbose_name='周boll发散')
    week_d=models.DecimalField(max_digits=5,decimal_places=1,verbose_name='周线KDJ的D值')
    week_k=models.DecimalField(max_digits=5,decimal_places=1,verbose_name='周线KDJ的K值')
    week_deviation = models.CharField(max_length=16, verbose_name='周线MACD背离')
    week_macd_trend = models.CharField(max_length=16, verbose_name='周线MACD趋势')
    week_ma_trend = models.CharField(max_length=16, verbose_name='周线MA20趋势')
    week_swing_vol = models.CharField(max_length=16, verbose_name='周线量价异常')
    week_ma_20=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='周20均线值')

    day_boll_up=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='日线boll下轨')
    day_boll_low=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='日线boll下轨')
    day_boll_sd = models.CharField(max_length=16, verbose_name='日boll发散')
    day_d = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='日线KDJ的D值')
    day_k = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='日线KDJ的K值')
    day_deviation = models.CharField(max_length=16, verbose_name='日线MACD背离')
    day_macd_trend = models.CharField(max_length=16, verbose_name='日线MACD趋势')
    day_ma_trend = models.CharField(max_length=16, verbose_name='日线MA20趋势')
    day_ma_20 = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='日20均线值')
    day_swing_vol=models.CharField(max_length=16, verbose_name='日线量价异常')

    now_price=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='现价')


class FinanceCheck(BaseModel):
    """财务指标诊断"""
    pass