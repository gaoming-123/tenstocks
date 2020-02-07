import datetime

import pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from login.models import Users, ConfirmString
from login.utils import login, set_password, make_confirm_string, send_email, check_login
from tenstocks.settings import TIME_ZONE
from .forms import LoginForm, RegisterForm
from .settings import CONFIRM_DAYS,EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
# Create your views here.


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    def post(self, request):
        login_form = LoginForm(request.POST)
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
                return redirect('login:info')
        else:
            return render(request, 'login/login.html', {'form': login_form})


class Register(View):
    def get(self, request):
        form = RegisterForm()

        return render(request, 'login/register.html', {'form': form})

    def post(self, request):

        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            cleaned_data = reg_form.cleaned_data
            user = Users()
            user.phone = cleaned_data.get('phone')
            user.nickname = cleaned_data.get('nickname')
            user.password = set_password(cleaned_data.get('password2'))
            user.save()
            login(request, user)
            return redirect('login:info')
        else:
            return render(request, 'login/register.html', {'form': reg_form})


class InfoView(View):
    """个人资料"""
    @check_login
    def get(self, request):
        pk = request.session.get('ID')
        user = Users.objects.filter(id=pk)[0]
        context = {
            'nickname': user.nickname if user.nickname else request.session.get('nickname'),
            'email': user.email if user.email else '',
            'sign': user.sign,
        }
        return render(request, 'login/info.html', context=context)

    def post(self, request):
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        same_email_user = Users.objects.filter(email=email)
        if email and same_email_user:
            message = '该邮箱已经被注册了！'
            return render(request, 'login/info.html', locals())
        sign = request.POST.get('sign')
        pk = request.session.get('ID')
        result = Users.objects.filter(id=pk).update(nickname=nickname, email=email, sign=sign)
        user = Users.objects.filter(id=pk)[0]
        if result:
            message = '修改成功!'
            if email:
                code = make_confirm_string(user)
                send_email(email, code)
                message = '修改成功,请前往邮箱进行确认！'
            context = {
                'nickname': nickname,
                'email': email,
                'sign': sign,
                'message': message,
            }
        else:
            user = Users.objects.filter(id=pk)[0]
            context = {
                'nickname': user.nickname,
                'email': user.email if user.email else '',
                'sign': user.sign,
                'messsge': '未修改成功！'
            }
        return render(request, 'login/info.html', context=context)


class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone(TIME_ZONE))
    if now > c_time + datetime.timedelta(CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def send_my_email(request):
    if request.method=='GET':
        from django.core.mail import send_mail
        send_mail(
            'tenstocks',
            'Here is the message.',
            EMAIL_HOST_USER,
            ['451574449@qq.com'],
            fail_silently=False,
        )
        return HttpResponse('send email success')