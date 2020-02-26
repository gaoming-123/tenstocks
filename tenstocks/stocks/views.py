import datetime
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from calculator.calcu import pe_pick
from calculator.pick import stock_pick, pick_buy, pick_buy_or_sell
from .utils import add_money_out_data, get_all_stocks, get_five_day_data, get_rongzirongquan_from_dfcf, get_all_rzrq, \
    get_week_sh_sz, get_finance_quota_from_tushare, get_stock_trade_data, get_finance_quota_stock, \
    get_market_day_quota, get_market_rzrq, check_stock_exist
from .models import UserStocks, A_stocks, Money_out, WeekCompany, RzRq, FinanceQuota, TradeData, MarketDayQuota, \
    MonthCapitalSettlement


class Stocks(generic.View):
    def get(self, request):
        # pk=request.session.get("ID")
        # user_stocks=UserStocks.objects.filter(user=pk)
        # context={
        #     'stocks':user_stocks
        # }
        # return render(request,'stocks/首页',context=context)
        return render(request, 'stocks/index.html')


class Add_stock(generic.View):
    def post(self, request):
        stock_code = request.POST.get('stock_code')
        # for code_end in ['.SH','.SZ']:
        stock = A_stocks.objects.filter(symbol=stock_code)
        if stock:
            pk = request.session.get("ID")
            user_stocks = UserStocks.objects.create(user=pk, stock=stock, stock_code=stock_code)
            # 返回到列表首页
            return render(request, 'stocks/index.html')
        else:
            # 返回错误  股票代码输入错误，请输入正确的6位股票代码
            pass
        # 添加
        pass


class Add_first_data(generic.View):
    def get(self, request):
        add_money_out_data()
        return HttpResponse('add 五日资金流及公司 data success')


class New_stocks(generic.View):
    def get(self, request):
        get_all_stocks()
        return HttpResponse('add A股股票 data success')


class Stock_dfcf_RzRq(generic.View):
    def get(self, request, code):
        stock = check_stock_exist(code)
        if not stock:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        get_rongzirongquan_from_dfcf(stock=stock, all=True)
        return HttpResponse(f'从东方财富 add {code} 融资融券成功')


class Stock_tushare_RzRq(generic.View):
    def get(self, request):
        start_time = time.time()
        get_all_rzrq()
        return HttpResponse(f'add 融资融券 添加历史数据成功 花费{time.time()-start_time}秒')


class Five_day_data(generic.View):
    def get(self, request):
        money, company = get_five_day_data()
        l_money = len(money)
        l_company = len(company)
        money['week_sub'] = sum(money.values())  # 资金总和
        week_sh, week_sz, week_h_z, c_time = get_week_sh_sz()
        money['c_time'] = c_time
        money['money_out_rate'] = abs(round(money['week_sub'] / week_h_z * 100, 3))
        money['week_sh'] = week_sh
        money['week_sz'] = week_sz
        money['week_h_z'] = week_h_z
        company['c_time'] = c_time
        Money_out.objects.create(**money)
        WeekCompany.objects.create(**company)
        # print(money)
        return HttpResponse(f'add 五日资金流及公司 date {c_time} data: money{l_money}条 company {l_company}个  success')
        # return HttpResponse(f'add 五日资金流及公司 data: money{money} company {company}  success')


class Monitor(generic.View):
    def get(self, request):
        all_data = Money_out.objects.all().order_by('c_time')
        market = MarketDayQuota.objects.all().order_by('trade_date')
        money = MonthCapitalSettlement.objects.all().order_by('trade_date')
        print(len(market))
        context = {
            'datas': [[str(data.c_time), float(data.money_out_rate), -float(data.week_sub)] for data in all_data],

            'markets': [[str(m.trade_date), round(m.day_mid_amount,4), m.day_mid_pe, m.day_mid_pe_ttm,
                         round(m.day_mid_pb,4), m.day_low_10, m.day_up_10, round(m.turnover_rate_f,4),
                         round(m.turnover_rate,4), m.pb_lt_1, m.sh_rzrqye, m.sz_rzrqye, m.sh_rqye, m.sz_rqye] for m in market if
                        m.sh_rzrqye],
            'money':[[str(mo.trade_date),float(mo.us_money_net)] for mo in money],
        }

        return render(request, 'stocks/monitor.html', context=context)


class Finance_quota(generic.View):
    def get(self, request, code):
        try:
            stock = A_stocks.objects.filter(symbol=code)[0]
        except:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        data = get_finance_quota_from_tushare(stock.ts_code)
        for da in data:
            FinanceQuota.objects.create(**da)
        return HttpResponse(f'add stock: {code}财务指标 data：{len(data)}条 success 添加历史数据成功 ')


class StockDetail(generic.View):
    def get(self, request, code):
        try:
            stock = A_stocks.objects.filter(symbol=code)[0]
        except:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        # 交易数据
        trade_datas = TradeData.objects.filter(stock=stock).order_by('trade_date')
        trade_data = [[str(t.trade_date), t.close, t.amount / 10] for t in trade_datas]
        # 融资融券数据
        rzrqs = RzRq.objects.filter(stock=stock).order_by('trade_date')
        rzrq = [[str(r.trade_date), r.spj, r.rzrqye, r.rzyezb] for r in rzrqs]
        # 指标数据
        fin_datas = FinanceQuota.objects.filter(ts_code=stock.ts_code).order_by('end_date')
        # 报告期，销售净利率,扣非净利润,净资产收益率(单季度),营业总收入同比增长率
        fin_data = [[str(f.end_date),
                     f.netprofit_margin if f.netprofit_margin else 0,
                     f.profit_dedt if f.profit_dedt else 0,
                     f.q_roe if f.q_roe else 0,
                     f.tr_yoy if f.tr_yoy else 0, ] for f in fin_datas]

        # 返回详情页内容
        return render(request, 'stocks/detail.html', context=locals())


class StockTradeData(generic.View):
    def get(self, request, code):
        try:
            stock = A_stocks.objects.filter(symbol=code)[0]
        except:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        # 获取交易数据保存到数据库
        res = get_stock_trade_data(stock)
        if res:
            return HttpResponse(f'添加{code} daily 交易数据成功')
        else:
            return HttpResponse(f'添加{code} daily 交易数据失败')


class PickStock(generic.View):
    def get(self, request):
        # stocks = A_stocks.objects.all()
        stocks=pe_pick(date_day='20200110',pe=30)
        print(len(stocks))
        # stocks=pe_pick()
        # stocks=['002539.SZ','000407.SZ','601368.SH','300196.SZ']
        res = pick_buy_or_sell(stocks, period='week')
        for ke in res.keys():
            print(ke,len(res[ke]))
        today=str(datetime.date.today()).replace('-','')
        for i in range(-7, 8):
            if res[str(i)]:
                with open(f'E:\myprojects\\tenstocks\pick_result\\{today}result_{i}.txt', 'w', encoding='utf-8') as f:
                    f.write(','.join(res[str(i)]))
        return HttpResponse(f'完成今日股票筛选{res}')


class TradeStock(generic.View):
    def get(self, request, code):
        try:
            stock = A_stocks.objects.filter(symbol=code)[0]
        except:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        res = stock_pick(code, asset='E', period='day')
        return HttpResponse(f'完成今日股票筛选{res}')


class Test(generic.View):
    def get(self, request):
        start = time.time()
        # pe_pick()
        end = time.time() - start
        return HttpResponse(f'test--{end/60}分-完成--ok')


class GetFinanceQuota(generic.View):
    def get(self, request, code):
        try:
            stock = A_stocks.objects.filter(symbol=code)[0]
        except:
            return HttpResponse('add A股股票 data fail,请检查你的输入')
        res = get_finance_quota_stock(stock.ts_code)
        return HttpResponse(f'完成今日股票筛选{res}')


# 计算全市场每日指标数据
class CalcuMarketDayQuota(generic.View):
    def get(self, request):
        last_market_day = MarketDayQuota.objects.all().order_by('-trade_date')[0]
        first_start=start = str(last_market_day.trade_date)
        # first_start=start='2010-06-25'
        today = str(datetime.date.today())
        # print(today)
        while start != today:
            start_day = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=1)
            start_day = start_day.date().strftime('%Y-%m-%d')
            try:
                res = get_market_day_quota(start_day)
            except Exception as e:
                print(e)
            finally:
                start = start_day
        # 融资融券数据
        get_market_rzrq()
        return HttpResponse(f'add data  {first_start} to {today} success')
