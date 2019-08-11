# encoding: utf-8
# author:  gao-ming
# time:  2019/7/20--16:20
# desc:
import hashlib

from django.http import JsonResponse
from django.shortcuts import redirect

from tenstocks.settings import SECRET_KEY


def set_password(password):
    for _ in range(1000):
        pass_str = "{}{}".format(password, SECRET_KEY)
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
    def verify_login(request, *args, **kwargs):
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
                return redirect('user:登录')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login