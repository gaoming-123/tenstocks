# encoding: utf-8
# author:  gao-ming
# time:  2019/7/20--16:20
# desc:
import datetime
import hashlib

from django.http import JsonResponse
from django.shortcuts import redirect

from login.models import ConfirmString
from .settings import *



def set_password(password,salt=SECRET_KEY):
    for _ in range(1000):
        pass_str = "{}{}".format(password, salt)
        h = hashlib.md5(pass_str.encode('utf-8'))
        password = h.hexdigest()
    return password


def login(request, user):  # 保存session的方法
    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session['nickname'] = user.nickname if user.nickname else f'用户{user.phone[0:5]}****{user.phone[-2:]}'
    request.session['phone'] = user.phone
    # request.session['head'] = user.head
    request.session.set_expiry(0)  # 关闭浏览器就消失


def check_login(func):  # 登录验证装饰器
    # 新函数
    def verify_login(self,request, *args, **kwargs):
        # 验证session中是否有登录标识
        if request.session.get("ID") is None:
            # 将上个请求地址保存到session
            referer = request.META.get('HTTP_REFERER',None)
            if referer:
                request.session['referer'] = referer

            # 判断 是否为ajax请求
            if request.is_ajax():
                return JsonResponse({'code':1,'message':'未登录'})
            else:
                return redirect('login')
        else:
            # 调用原函数
            return func(self,request, *args, **kwargs)

    # 返回新函数
    return verify_login


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = set_password(user.phone, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code



def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.tenstocks.com的注册确认邮件'

    text_content = '''感谢注册www.tenstocks.com，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/login/confirm/?code={}" target=blank>www.tenstocks.com</a>，\
                    tenstocks</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content,EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# def send_email_to_user():
#     import os
#     from django.core.mail import send_mail
#
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'