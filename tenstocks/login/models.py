from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class Users(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    phone = models.CharField(max_length=11, unique=True,
                             verbose_name="手机号码",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    nickname = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="昵称"
                                )
    email = models.EmailField(max_length=128, null=True, blank=True, unique=True,
                              verbose_name='邮箱')
    password = models.CharField("密码", max_length=128, )
    scores = models.IntegerField(default=50, verbose_name='积分')
    sign = models.CharField(max_length=128, default='很懒，什么也没留下！', verbose_name='签名')
    # 设置头像字段
    # head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")
    sex = models.CharField(max_length=8, choices=gender, default='男')

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    def __str__(self):
        return self.phone

    class Meta:
        # ordering=['-reg_time']
        db_table = "users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"