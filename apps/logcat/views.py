import datetime
from django.shortcuts import render
from apps.host.models import Host
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def system(request):
    """系统信息"""
    host = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.system_info.all()
        host.append(sys)
    mesnum = inbox(request)
    return render(request, 'system_table.html', locals())

@login_required
def version(request):
    """系统版本"""
    os = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.os_version.all()
        os.append(sys)
    mesnum = inbox(request)
    return render(request, 'version_table.html', locals())

@login_required
def memory(request):
    """内存信息"""
    memory = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.memory_info.all()
        memory.append(sys)
    mesnum = inbox(request)
    return render(request, 'memory_table.html', locals())

@login_required
def user(request):
    """主机用户"""
    user = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.log_user.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        user.append(sys)
    mesnum = inbox(request)
    return render(request, 'user_table.html', locals())

@login_required
def processes(request):
    """主机进程"""
    processes = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.processes.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        processes.append(sys)
    mesnum = inbox(request)
    return render(request, 'processes_table.html', locals())

@login_required
def crontab(request):
    """定时任务"""
    crontab = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.crontab.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        crontab.append(sys)
    mesnum = inbox(request)
    return render(request, 'crontab_table.html', locals())

@login_required
def hidden(request):
    """隐藏文件"""
    hidden = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.hidden.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        hidden.append(sys)
    mesnum = inbox(request)
    return render(request, 'hidden_table.html', locals())

@login_required
def shell_tty(request):
    """shell连接"""
    shell = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.shell_tty.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        shell.append(sys)
    mesnum = inbox(request)
    return render(request, 'shell_table.html', locals())

@login_required
def open_port(request):
    """端口开放"""
    open = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.open_port.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        open.append(sys)
    mesnum = inbox(request)
    return render(request, 'port_table.html', locals())

@login_required
def bean_shell(request):
    """反弹shell"""
    bean = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.bean_shell.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        bean.append(sys)
    mesnum = inbox(request)
    return render(request, 'bean_table.html', locals())

@login_required
def inbox(request):
    """消息流"""
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    mesnum = 0
    for h in hosts:
        num = h.log_user.filter(active=0).count()
        num = h.processes.filter(active=0).count() + num
        num = h.crontab.filter(active=0).count() + num
        num = h.hidden.filter(active=0).count() + num
        num = h.shell_tty.filter(active=0).count() + num
        num = h.open_port.filter(active=0).count() + num
        num = h.bean_shell.filter(active=0).count() + num
        num = h.file.filter(active=0).count() + num
        mesnum = mesnum + num
    return mesnum