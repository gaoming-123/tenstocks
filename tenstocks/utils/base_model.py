# encoding: utf-8
# author:  gao-ming
# time:  2019/7/20--15:45
# desc:

from django.db import models


class BaseModel(models.Model):
    """基础模型类,让所有的模型都能继承"""
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')  # 是否删除
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 设置当前类为抽象的类, 被迁移
        abstract = True
