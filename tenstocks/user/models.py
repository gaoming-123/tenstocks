from django.core.validators import RegexValidator
from django.db import models

# Create your models here.



from utils.base_model import BaseModel


class Users(BaseModel):
    """用户表"""
    phone = models.CharField(max_length=11,
                             verbose_name="手机号码",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    nickname = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="昵称"
                                )
    email=models.EmailField(max_length=50,null=True,blank=True,
                            verbose_name='邮箱')
    password = models.CharField(max_length=32,
                                verbose_name="密码"
                                )
    scores=models.IntegerField(default=50,verbose_name='积分')
    sign=models.CharField(max_length=64,default='很懒，什么也没留下！',verbose_name='签名')

    # 设置头像字段
    # head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name