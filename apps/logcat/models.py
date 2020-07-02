from django.db import models
from apps.host.models import Host
# Create your models here.


class System_info(models.Model):
    """获取的主机信息"""
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='system_info')
    computer_name = models.CharField(max_length=100, verbose_name='物理主机名', default='')
    cpu_brand = models.CharField(max_length=200, verbose_name='CPU信息')
    cpu_type = models.CharField(max_length=100, verbose_name='CPU类型')
    physical_memory = models.BigIntegerField(verbose_name='物理内存')

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.computer_name


class OS_version(models.Model):
    """获取内核信息"""
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='os_version')
    version = models.CharField(verbose_name='内核版本', max_length=100)
    arguments = models.CharField(verbose_name='内核参数', max_length=200)

    class  Meta:
        verbose_name = '内核信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


class Memory_info(models.Model):
    """内存信息"""
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='memory_info')
    memory_total = models.BigIntegerField(verbose_name='内存总量')
    memory_free = models.BigIntegerField(verbose_name='剩余总量')

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.memory_free)

class Log_user(models.Model):
    """用户信息"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='log_user')
    uid = models.IntegerField(verbose_name='UID')
    gid = models.IntegerField(verbose_name='GID')
    username = models.CharField(verbose_name='主机用户', max_length=100)
    description = models.CharField(verbose_name='类型', max_length=100)
    directory = models.CharField(verbose_name='用户目录', max_length=100)
    shell = models.CharField(max_length=100, verbose_name='shell类型')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Processes(models.Model):
    """进程信息"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='processes')
    pid  = models.CharField(max_length=200, verbose_name='PID')
    name = models.CharField(max_length=200, verbose_name='进程名')
    path = models.CharField(max_length=200, verbose_name='进程文件路径', default='')
    cmdline = models.CharField(max_length=10000, verbose_name='进行命令')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '进程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Crontab(models.Model):
    """计划任务"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='crontab')
    command = models.CharField(max_length=200, verbose_name='计划任务命令')
    path = models.CharField(max_length=200, verbose_name='计划任务路径')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '计划任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.command


class Hidden(models.Model):
    """查看用户隐藏文件"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='hidden')
    path = models.CharField(max_length=200, verbose_name='文件路径')
    filename = models.CharField(max_length=100, verbose_name='文件名')
    btime = models.CharField(max_length=100, verbose_name='文件创建时间')
    ctime = models.CharField(max_length=100, verbose_name='最后修改时间')
    sha1 = models.CharField(max_length=100, verbose_name='sha1', default='')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '隐藏文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.filename

class Shell_TTY(models.Model):
    """查看shell连接"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='shell_tty')
    name = models.CharField(max_length=100, verbose_name='连接名')
    path = models.CharField(max_length=200, verbose_name='连接路径')
    remote_address = models.CharField(max_length=100, verbose_name='远程连接')
    remote_port = models.CharField(max_length=100, verbose_name='远程端口')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '远程连接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Open_Port(models.Model):
    """查看端口开放"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='open_port')
    name = models.CharField(max_length=100, verbose_name='端口开放名')
    path = models.CharField(max_length=200, verbose_name='端口文件')
    port = models.IntegerField(verbose_name='开放端口')
    address = models.CharField(max_length=100, verbose_name='本地地址')
    pid = models.IntegerField(verbose_name='PID')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '端口开放'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Bean_shell(models.Model):
    """反弹shell"""
    AVATOR = (
        (0, '未读'),
        (1, '已读')
    )
    hostname = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机名', related_name='bean_shell')
    pid = models.IntegerField(verbose_name='PID')
    name = models.CharField(max_length=200, verbose_name='反弹类型')
    path = models.CharField(max_length=200, verbose_name='反弹文件路径')
    remote_address = models.CharField(max_length=200, verbose_name='远程地址')
    remote_port = models.IntegerField(verbose_name='远程端口')
    parent_cmdline = models.CharField(max_length=200, verbose_name='反弹命令')
    time = models.DateTimeField(verbose_name='添加时间', auto_now=True)
    active = models.IntegerField(verbose_name='消息状态', default=0, choices=AVATOR)

    class Meta:
        verbose_name = '反弹shell'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name