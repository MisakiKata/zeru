from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Host(models.Model):
    #主机信息
    AVATOR = {
        (1, '存活'),
        (2, '失效')
    }
    Auther = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='主机管理员')
    Hostname = models.GenericIPAddressField(verbose_name='主机地址')
    Email = models.EmailField(verbose_name='邮件地址')
    Active = models.IntegerField(choices=AVATOR, default=1, verbose_name='存活状态')

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Hostname


class Kafka(models.Model):
    """kafka地址"""
    AVATOR = (
        (1, '存活'),
        (2, '失效')
    )
    Kafka = models.CharField(max_length=100, verbose_name='Kafka地址')
    Active = models.IntegerField(verbose_name='是否存活', choices=AVATOR, default=1)


    class Meta:
        verbose_name = 'Kakfa地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Kafka