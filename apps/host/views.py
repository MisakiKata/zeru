from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apps.host.models import Host, Kafka
from apps.threat.models import FileMonitor, CVESerach
from django.contrib import auth
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    """登录"""
    if request.user.is_authenticated:
        return redirect('/index')
    else:
        user = request.POST.get('name')
        pwd = request.POST.get('passwd')
        user = auth.authenticate(request, username=user, password=pwd)
        if user:
            auth.login(request, user)
            return redirect('/index')
        return render(request, 'login.html', locals())

@login_required
def logout(request):
    """退出登录"""
    request.session.flush()
    return redirect('/login')

@login_required
def index(request):
    """首页图表"""

    echart1 = echarts1(request)
    echart2 = echarts2(request)
    echart4 = echarts4(request)
    mesnum = inbox(request)
    days = DataTableSort(15)
    return render(request, 'index.html', locals())

def echarts1(request):
    """饼图"""
    user = User.objects.get(username=request.user.username)
    host = Host.objects.filter(Auther=user)
    filenum, process, crontab, hidden, open_port = 0,0,0,0,0
    for h in host:
        num = FileMonitor.objects.filter(hostname=h).count() #文件变动总数
        filenum = filenum + num

        num = h.processes.all().count()  # 进程总数
        process = process + num

        num = h.crontab.all().count()
        crontab = crontab + num

        num = h.hidden.all().count()
        hidden = hidden + num

        num = h.open_port.all().count()
        open_port = open_port + num
    return [filenum, process, crontab, hidden, open_port]

def echarts2(request):
    """饼图2"""
    oneday = CVESerach.objects.filter(time__lt=datetime.datetime.now()).count()  #今天数据
    twoday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=1)).count()  #昨天数据
    threeday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=2)).count()  # 前天数据
    fourday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=3)).count()  # 四天数据
    fiveday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=4)).count()  # 五天数据
    sixday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=5)).count()  # 六天数据
    senday = CVESerach.objects.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=6)).count()  # 七天数据
    return [oneday, twoday, threeday, fourday, fiveday, sixday, senday]

def echarts4(request):
    """折线图"""
    filenum, process, crontab, hidden, open_port, shell_tty = [],[],[],[],[],[]
    for traversecity in CalculationsFor(request, 15):
        filenum.append(traversecity[0])
        process.append(traversecity[1])
        crontab.append(traversecity[2])
        hidden.append(traversecity[3])
        open_port.append(traversecity[4])
        shell_tty.append(traversecity[5])
    return {"filenum":filenum, "process":process, "crontab":crontab, "hidden":hidden, "open_port":open_port, "shell_tty":shell_tty}


def DataTableSort(num):
    days = []
    for d in range(0, num):
        day = (datetime.date.today() - datetime.timedelta(days=d)).__format__("%Y-%m-%d")
        days.append(day)
    return days


def CalculationsFor(request, num):
    """某个监控，某天的全部数量"""
    day_number = []
    user = User.objects.get(username=request.user.username)
    host = Host.objects.filter(Auther=user)
    for day in range(num):
        filenum, process, crontab, hidden, open_port, shell_tty = 0,0,0,0,0,0
        for h in host:
            number = h.processes.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            process = process + number
            number = FileMonitor.objects.filter(hostname=h,time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            filenum = filenum + number
            number = h.hidden.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            hidden = hidden + number
            number = h.open_port.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            open_port = open_port + number
            number = h.shell_tty.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            shell_tty = shell_tty + number
            number = h.crontab.filter(time__lt=datetime.datetime.now() - datetime.timedelta(days=day)).count()
            crontab = crontab + number
        day_number.append([filenum, process, crontab, hidden, open_port, shell_tty])
    return day_number

@login_required
def host(request):
    """主机信息"""
    user_id = User.objects.filter(username=request.user.username)[0]
    hosts = Host.objects.filter(Auther_id=user_id)
    mesnum = inbox(request)
    return render(request, 'host_table.html', locals())

@login_required
def profile(request):
    """显示信息"""
    mesnum = inbox(request)
    return render(request, 'profile.html', locals())

@login_required
def edit_profile(request):
    """编辑设置信息"""
    if request.method == 'GET':
        mesnum = inbox(request)
        return render(request, 'profile-edit.html', {'mesnum':mesnum})
    elif request.method == 'POST':
        kafka = request.POST.get('kafka')
        hostip = request.POST.get('hostip')
        if kafka != '':
            for k in kafka.split('\n'):
                Kafka.objects.create(Kafka=k, Active=1)
        if hostip != '':
            for ip in hostip.split('\n'):
                user_id = User.objects.get(username=request.user.username)
                Host.objects.create(Auther=user_id, Hostname=ip, Email='', Active=1)
        else:
            mesnum = inbox(request)
            return render(request, 'profile-edit.html', {'mesnum':mesnum})
        message = '保存成功'
        mesnum = inbox(request)
        return render(request, 'profile-edit.html', locals())

@login_required
def passwd(request):
    """更改密码"""
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('passwd')
        new_password = request.POST.get('newpasswd')
        repeat_password = request.POST.get('newpasswd2')
        if user.check_password(old_password):
            if not new_password:
                err_msg = '新密码不能为空'
            elif new_password != repeat_password:
                err_msg = '两次密码不一致'
            else:
                user.set_password(new_password)
                user.save()
                suc_msg = '密码更改成功'
                return render(request, 'profile-edit.html', locals())
        else:
            err_msg = '原密码输入错误'
    mesnum = inbox(request)
    return render(request, 'profile-edit.html', locals())


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


def page_not_found(request, exception):
    """404"""
    return render(request, '404.html')


def page_error(request):
    """500"""
    return render(request, '500.html')


