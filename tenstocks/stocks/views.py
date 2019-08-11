from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic

from .utils import add_money_out_data, get_all_stocks
from .models import UserStocks,A_stocks


class Stocks(generic.View):
    def get(self,request):
        # pk=request.session.get("ID")
        # user_stocks=UserStocks.objects.filter(user=pk)
        # context={
        #     'stocks':user_stocks
        # }
        # return render(request,'stocks/首页',context=context)
        return render(request,'stocks/index.html')



class Add_stock(generic.View):
    def post(self,request):
        stock_code=request.POST.get('stock_code')
        # for code_end in ['.SH','.SZ']:
        stock=A_stocks.objects.filter(symbol=stock_code)
        if stock:
            pk=request.session.get("ID")
            user_stocks=UserStocks.objects.create(user=pk,stock=stock,stock_code=stock_code)
            # 返回到列表首页
            return render(request,'stocks/index.html')
        else:
            # 返回错误  股票代码输入错误，请输入正确的6位股票代码
            pass
        # 添加
        pass



class Add_first_data(generic.View):
    def get(self,request):
        add_money_out_data()
        return HttpResponse('add 五日资金流及公司 data success')

class New_stocks(generic.View):
    def get(self,request):
        get_all_stocks()
        return HttpResponse('add A股股票 data success')

