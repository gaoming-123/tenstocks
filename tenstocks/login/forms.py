# encoding: utf-8
# author:  gao-ming
# time:  2019/7/20--16:12
# desc:
import re

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from django import forms


from .models import Users
from .utils import set_password


class RegisterForm(forms.ModelForm):
    """注册表单, 验证"""
    # 单独添加字段
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码长度不能大于16个字符',
                                    'min_length': '密码长度必须大于6个字符',
                                }
                                )
    password2 = forms.CharField(error_messages={'required': "确认密码必填"})

    # # 验证码
    # captcha = forms.CharField(max_length=6,
    #                           error_messages={
    #                               'required': "验证码必须填写"
    #                           })
    captcha = CaptchaField(label='验证码')

    # agree = forms.BooleanField(error_messages={
    #     'required': '必须同意用户协议'
    # })

    class Meta:
        model = Users
        # 需要验证的字段
        fields = ['phone', ]

        error_messages = {
            "phone": {
                "required": "手机号码必须填写!"
            }
        }

    def clean_phone(self):
        # 验证手机号码是否唯一
        phone = self.cleaned_data.get('phone')
        try:
            phone = re.findall(r'^1[3-9]\d{9}$', phone)[0]
            print(phone)
        except:
            raise forms.ValidationError("手机号码格式不正确！")
        if phone != self.cleaned_data.get('phone'):
            raise forms.ValidationError("手机号码格式不正确！")
        rs = Users.objects.filter(phone=phone).exists()  # 返回bool
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        print('lllll')
        return phone

    # def clean_captcha(self):
    #     captcha_str = self.cleaned_data.get('captcha_1')
    #     captcha_haskey = self.cleaned_data.get('captcha_0')
    #     if captcha_str and captcha_haskey:
    #         try:
    #             get_captcha = CaptchaStore.objects.get(hashkey=captcha_haskey)
    #             if get_captcha.response == captcha_str.lower():
    #                 return captcha_str
    #         except:
    #             raise forms.ValidationError('验证码错误！')
    #     else:
    #         raise forms.ValidationError('验证码错误！')

    def clean(self):
        # 验证两个密码是否一致
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            # 确认密码错误
            raise forms.ValidationError({"password2": "两次密码输入不一致!"})

        # 综合校验
        # 验证 用户传入的验证码和redis中的是否一样
        # 用户传入的
        # try:
        #     captcha = self.cleaned_data.get('captcha')
        #     phone = self.cleaned_data.get('phone','')
        #     # 获取redis中的
        #     r = get_redis_connection()
        #     random_code = r.get(phone)  # 二进制, 转码
        #     random_code = random_code.decode('utf-8')
        #     # 比对
        #     if captcha and captcha != random_code:
        #         raise forms.ValidationError({"captcha": "验证码输入错误!"})
        # except:
        #     raise forms.ValidationError({"captcha": "验证码输入错误!"})
        phone=self.cleaned_data['phone']
        self.cleaned_data['nickname']=f'用户{phone[0:5]}****{phone[-2:]}'
        # 返回清洗后的所有数据
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    captcha = CaptchaField(label='验证码')
    class Meta:
        model = Users
        fields = ['phone', 'password']

        error_messages = {
            'phone': {
                'required': '请填写手机号',
            },
            'password': {
                'required': '请填写密码',
            }
        }
    # def clean_captcha(self):
    #     captcha_str = self.cleaned_data.get('captcha_1')
    #     captcha_haskey = self.cleaned_data.get('captcha_0')
    #     if captcha_str and captcha_haskey:
    #         try:
    #             get_captcha = CaptchaStore.objects.get(hashkey=captcha_haskey)
    #             if get_captcha.response == captcha_str.lower():
    #                 return captcha_str
    #         except:
    #             raise forms.ValidationError('验证码错误！')
    #     else:
    #         raise forms.ValidationError('验证码错误！')

    def clean(self):
        # 获取用户名和密码
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            raise forms.ValidationError({'phone': '手机号错误'})
        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写错误'})
        # 将用户信息保存到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data
