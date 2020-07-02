from django.db import models
from apps.host.models import Host
from django.contrib.auth.models import User
# Create your models here.


class FileMonitor(models.Model):
    """文件监控"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='file')
    action = models.CharField(max_length=100, verbose_name='文件行为')
    atime = models.CharField(max_length=100, verbose_name='文件访问时间')
    ctime = models.CharField(max_length=100, verbose_name='权限修改时间')
    mtime = models.CharField(max_length=100, verbose_name='内容修改时间')
    sha1 = models.CharField(max_length=100, verbose_name='文件hash值', default='')
    size = models.CharField(max_length=100, verbose_name='文件大小')
    target_path = models.CharField(max_length=200, verbose_name='文件路径')
    uid = models.CharField(max_length=10, verbose_name='文件用户UID')
    gid = models.CharField(max_length=10, verbose_name='文件用户组GID')
    mode = models.CharField(max_length=10, verbose_name='文件权限')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '文件监控'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.target_path


class CVESerach(models.Model):
    """cve监控"""
    publish = models.CharField(max_length=50, verbose_name='更新时间')
    cvss = models.FloatField(verbose_name='评分(max=5.0)')
    cwe = models.CharField(max_length=20, verbose_name='CWE编号')
    cve = models.CharField(max_length=30, verbose_name='CVE编号')
    references = models.TextField(max_length=500, verbose_name='详情地址')
    summary = models.CharField(max_length=10000, verbose_name='漏洞描述')
    time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = 'CVE监控'
        verbose_name_plural =verbose_name

    def __str__(self):
        return self.cve


class KeyName(models.Model):
    """CVE筛选关键词"""
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    keyname = models.CharField(max_length=100, verbose_name='筛选关键词')

    class Meta:
        verbose_name = '筛选关键词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keyname