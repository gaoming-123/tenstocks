from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
# Create your views here.
from user.forms import LoginModelForm, RegisterModelForm
from user.models import Users
from user.utils import login, set_password


class LoginView(generic.View):
    """登录"""
    def get(self,request):

        return render(request,'user/login.html')


    def post(self,request):
        data = request.POST
        login_form = LoginModelForm(data)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)

            referer = request.session.get('referer')
            if referer:
                # 跳转回去
                # 删除session
                del request.session['referer']
                return redirect(referer)
            else:
                return redirect('stocks:首页')
        else:
            return render(request, 'user/login.html', {'form': login_form})

class RegisterView(generic.View):
    """注册"""
    def get(self,request):
        return render(request,'user/register.html')


    def post(self,request):
        data = request.POST
        register_form = RegisterModelForm(data)
        if register_form.is_valid():
            cleaned_data = register_form.cleaned_data
            user = Users()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password2'))
            user.save()

            return redirect('user:个人资料')
        else:
            return render(request, 'user/register.html', {'form': register_form})



class InfoView(generic.View):
    """个人资料"""
    def get(self,request):
        pk = request.session.get('ID')
        user=Users.objects.filter(id=pk)
        context={
            'nickname':user.nickname,
            'email':user.email,
            'sign':user.sign,
        }
        return render(request,'user/info.html',context=context)
    def post(self,request):
        nickname=request.POST.get('nickname')
        email=request.POST.get('email')
        sign=request.POST.get('sign')
        pk=request.session.get('ID')
        result=Users.objects.filter(id=pk).update(nickname=nickname,email=email,sign=sign)
        if result:
            context = {
                'nickname': nickname,
                'email': email,
                'sign': sign,
                'messsge':'修改成功！'
            }
        else:
            user=Users.objects.filter(id=pk)
            context={
                'nickname': user.nickname,
                'email': user.email,
                'sign': user.sign,
                'messsge': '未修改成功！'
            }
        return render(request, 'user/info.html', context=context)


class RePasswordView(generic.View):
    """更改密码"""
    def get(self,request):
        pass
    def post(self,request):

        pass