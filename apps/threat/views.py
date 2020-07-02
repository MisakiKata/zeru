from django.shortcuts import render, redirect, HttpResponse
from apps.host.models import Host,Kafka
from kafka import KafkaConsumer
import apps.logcat.models as md
from apps.threat.models import FileMonitor, CVESerach, KeyName
from django.contrib.auth.models import User
import json, ares, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def filemonitor(request):
    """文件监控"""
    file = []
    username = User.objects.get(username=request.user.username)
    hosts = Host.objects.filter(Auther=username)
    for h in hosts:
        sys = h.file.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
        file.append(sys)
    mesnum = fileinbox(request)
    return render(request, 'filemonitor.html', locals())

@login_required
def fileinbox(request):
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

def run():
    host = []
    kafka = Kafka.objects.filter(Active=1)
    for k in kafka:
        host.append(k.Kafka.strip())

    consumer = KafkaConsumer(
        group_id="user-zeru",
        bootstrap_servers=host,
        value_deserializer=lambda m: json.loads(m.decode('ascii'))
    )
    consumer.subscribe(topics=('System_info','OS_version','Memory_info','Log_user','Processes','Crontab','Hidden','Shell_TTY',
                               'Open_Port','Bean_shell','Filemonitor'))
    for message in consumer:
        save(message.topic, message.value)

    consumer.commit_async()

def save(topic, value):
    host = Host.objects.get(Hostname=value['hostip'])

    if len(value) == 0:
        return
    if topic == 'System_info':
        if len(md.System_info.objects.filter(hostname=host)) == 0:
            md.System_info.objects.create(hostname=host, computer_name=value['computer_name'],
                                          cpu_brand=value['cpu_brand'], cpu_type=value['cpu_type'],
                                          physical_memory=int(value['physical_memory']))
        else:
            md.System_info.objects.filter(hostname=host).update(hostname=host, computer_name=value['computer_name'],
                                                                cpu_brand=value['cpu_brand'], cpu_type=value['cpu_type'],
                                                                physical_memory=int(value['physical_memory']))

    elif topic == 'OS_version':
        if len(md.OS_version.objects.filter(hostname=host)) == 0:
            md.OS_version.objects.create(hostname=host, version=value['version'], arguments=value['name'])
        else:
            md.OS_version.objects.filter(hostname=host).update(hostname=host, version=value['version'], arguments=value['name'])

    elif topic == 'Memory_info':
        if len(md.Memory_info.objects.filter(hostname=host)) == 0:
            md.Memory_info.objects.create(hostname=host, memory_total=int(value['memory_total']),
                                          memory_free=int(value['memory_free']))
        else:
            md.Memory_info.objects.filter(hostname=host).update(hostname=host, memory_total=int(value['memory_total']),
                                          memory_free=int(value['memory_free']))

    elif topic == 'Log_user':
        if len(md.Log_user.objects.filter(hostname=host, uid=int(value['uid']), username=value['username'])) == 0:
            md.Log_user.objects.create(hostname=host, uid=int(value['uid']), gid=int(value['gid']),
                                       username=value['username'],description=value['description'],
                                       directory=value['directory'], shell=value['shell'])
        else:
            md.Log_user.objects.filter(hostname=host, uid=int(value['uid']), username=value['username']).update(hostname=host,
                                       uid=int(value['uid']), gid=int(value['gid']),
                                       username=value['username'],description=value['description'],
                                       directory=value['directory'], shell=value['shell'])

    elif topic == 'Processes':
        if len(md.Processes.objects.filter(hostname=host,cmdline=value['cmdline'], name=value['name'])) == 0:
            md.Processes.objects.create(hostname=host, pid=value['pid'],name=value['name'],
                                        path=value['path'], cmdline=value['cmdline'])
        else:
            md.Processes.objects.filter(hostname=host,cmdline=value['cmdline'], name=value['name']).update(hostname=host,
                                        pid=value['pid'], name=value['name'],
                                        path=value['path'], cmdline=value['cmdline'])


    elif topic == 'Crontab':
        if len(md.Crontab.objects.filter(hostname=host, command=value['command'], path=value['path'])) == 0:
            md.Crontab.objects.create(hostname=host, command=value['command'], path=value['path'])
        else:
            md.Crontab.objects.filter(hostname=host, command=value['command'], path=value['path']).update(
                hostname=host, command=value['command'], path=value['path'])

    elif topic == 'Hidden':
        if len(md.Hidden.objects.filter(hostname=host, filename=value['filename'])) == 0:
            md.Hidden.objects.create(hostname=host, path=value['path'], filename=value['filename'],
                                 btime=value['btime'], ctime=value['ctime'], sha1=value['sha1'])
        else:
            md.Hidden.objects.filter(hostname=host, sha1=value['sha1']).update(hostname=host, path=value['path'],
                                    filename=value['filename'],btime=value['btime'], ctime=value['ctime'], sha1=value['sha1'])

    elif topic == 'Shell_TTY':
        if len(md.Shell_TTY.objects.filter(hostname=host, name=value['name'], path=value['path'])) == 0:
            md.Shell_TTY.objects.create(hostname=host, name=value['name'], path=value['path'],
                                    remote_address=value['remote_address'], remote_port=value['remote_port'])
        else:
            md.Shell_TTY.objects.filter(hostname=host, name=value['name'], path=value['path']).update(
                                        hostname=host, name=value['name'], path=value['path'],
                                        remote_address=value['remote_address'], remote_port=value['remote_port'])

    elif topic == 'Open_Port':
        if len(md.Open_Port.objects.filter(hostname=host, name=value['name'],port=int(value['port']))) == 0:
            md.Open_Port.objects.create(hostname=host, name=value['name'],path=value['path'],
                                    port=int(value['port']), address=value['address'], pid=int(value['pid']))
        else:
            md.Open_Port.objects.filter(hostname=host, name=value['name'],port=int(value['port'])).update(hostname=host,
                                        name=value['name'], path=value['path'],
                                        port=int(value['port']), address=value['address'], pid=int(value['pid']))

    elif topic == 'Bean_shell':
        if len(md.Bean_shell.objects.filter(hostname=host, pid=int(value['pid']), name=value['name'])) == 0:
            md.Bean_shell.objects.create(hostname=host, pid=int(value['pid']), name=value['name'],
                                     path=value['path'], remote_address=value['remote_address'],
                                     remote_port=int(value['remote_port']),parent_cmdline=value['parent_cmdline'])
        else:
            md.Bean_shell.objects.filter(hostname=host, pid=int(value['pid']), name=value['name']).update(hostname=host,
                                        pid=int(value['pid']), name=value['name'],path=value['path'], remote_address=value['remote_address'],
                                        remote_port=int(value['remote_port']), parent_cmdline=value['parent_cmdline'])

    elif topic == 'Filemonitor':
        if PAD_FILTER(host, value['columns']['uid']):
            if len(FileMonitor.objects.filter(hostname=host, action=value['columns']['action'],
                                                           sha1=value['columns']['sha1'])) == 0:
                FileMonitor.objects.create(hostname=host, action=value['columns']['action'], atime=unixtotime(value['columns']['atime']),
                                       ctime=unixtotime(value['columns']['ctime']), mtime=unixtotime(value['columns']['mtime']),sha1=value['columns']['sha1'],
                                       size=value['columns']['size'], target_path=value['columns']['target_path'],
                                       uid=value['columns']['uid'],gid=value['columns']['gid'],mode=value['columns']['mode'])
            else:
                FileMonitor.objects.filter(hostname=host, action=value['columns']['action'], sha1=value['columns']['sha1']).update(
                                        hostname=host, action=value['columns']['action'],atime=unixtotime(value['columns']['atime']),
                                        ctime=unixtotime(value['columns']['ctime']), mtime=unixtotime(value['columns']['mtime']),sha1=value['columns']['sha1'],
                                        size=value['columns']['size'], target_path=value['columns']['target_path'],uid=value['columns']['uid'],
                                        gid=value['columns']['gid'],mode=value['columns']['mode'])

import time
def unixtotime(date):
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(eval(date)))


def PAD_FILTER(host, uid):
    """文件过滤"""
    if md.Log_user.objects.filter(hostname=host, uid=int(uid)):
        shell = md.Log_user.objects.filter(hostname=host, uid=int(uid)).values('shell')[0]['shell']
        if shell == "/sbin/nologin" or shell == "/bin/false" or shell == "/usr/sbin/nologin":
            return True
        else:
            return False
    else:
        return False

@login_required
def Message_save(request):
    """定时任务"""
    user_id = User.objects.get(username=request.user.username)
    if request.GET.get('comshow'):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.start()
        register_events(scheduler)
        if request.GET.get('comshow') == 'yes':
            scheduler.add_job(run, 'interval', minutes=10, id='kafkajob')
            scheduler.add_job(cvesearch, 'interval', minutes=120, id='cvejob')
            scheduler.add_job(active_host, args=(user_id,), trigger='interval', minutes=60, id='hostjob')

        elif request.GET.get('comshow') == 'no':
            scheduler.remove_job('kafkajob')
            scheduler.remove_job('cvejob')
            scheduler.remove_job('hostjob')
        return redirect('/host/profile')
    else:
        return redirect('/index')

import subprocess

def active_host(user_id):
    """主机存活探测"""
    hosts = Host.objects.filter(Auther=user_id)
    for h in hosts:
        p = subprocess.Popen(['ping','-c','1', str(h.Hostname)], stdout=subprocess.PIPE)
        if p.poll():
            Host.objects.filter(Hostname=h.Hostname, Auther=user_id).update(Active=2)
        else:
            Host.objects.filter(Hostname=h.Hostname, Auther=user_id).update(Active=1)

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

    loguser, processes, crontab, hidden, shell, open_port, bean_shell, filemonitor = [],[],[],[],[],[],[],[]
    for h in hosts:
        me = h.log_user.filter(active=0)
        loguser.append(me)

        me = h.processes.filter(active=0)
        processes.append(me)

        me = h.crontab.filter(active=0)
        crontab.append(me)

        me = h.hidden.filter(active=0)
        hidden.append(me)

        me = h.open_port.filter(active=0)
        open_port.append(me)

        me = h.bean_shell.filter(active=0)
        bean_shell.append(me)

        me = h.shell_tty.filter(active=0)
        shell.append(me)

        me = h.file.filter(active=0)
        filemonitor.append(me)

    return render(request, 'inbox.html', locals())


@login_required
def inboxmess(request):
    """消息"""
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


@csrf_exempt
@login_required
def read(request):
    """消息已读"""
    if request.method == 'POST':
        id = request.POST.get('id')
        db = request.POST.get('db')
        if db == 'loguser':
            user = md.Log_user.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'filemonitor':
            user = FileMonitor.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'processes':
            user = md.Processes.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'crontab':
            user = md.Crontab.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'hidden':
            user = md.Hidden.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'bean_shell':
            user = md.Bean_shell.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'shell':
            user = md.Shell_TTY.objects.get(id=id)
            user.active = 1
            user.save()
        elif db == 'open_port':
            user = md.Open_Port.objects.get(id=id)
            user.active = 1
            user.save()
        return HttpResponse('更新成功')
    else:
        return HttpResponse('更新失败')


def cvesearch():
    """保存cve"""
    cve = ares.CVESearch()
    for sortBy in cve.last('30'):
        if len(CVESerach.objects.filter(cve=sortBy['id'])) == 0:
            references = "\n".join(sortBy['references'])
            CVESerach.objects.create(publish=sortBy['Published'].replace("T"," "), cvss=sortBy['cvss'], cve=sortBy['id'],cwe=sortBy['cwe'],
                                     references=references,summary=sortBy['summary'])

@login_required
def cve(request):
    """显示cve"""
    cveid = []
    user = User.objects.get(username=request.user.username)
    key = KeyName.objects.filter(user=user)
    inb = inboxmess(request)
    if len(key) != 0:
        for k in key:
            c = CVESerach.objects.filter(summary__contains=k, time__gt=datetime.datetime.now()-datetime.timedelta(days=7)).values_list('id')
            cveid.append(list(c))
        wordbyletter = []
        for mk in cveid:
            for mkk in mk:
                wordbyletter.append(mkk[0])
        wordbyletter = list(set(wordbyletter))
        cve = CVESerach.objects.filter(id__in=wordbyletter, time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
    else:
        cve = CVESerach.objects.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=7))
    return render(request, 'cve.html', locals())


@csrf_exempt
@login_required
def definekey(request):
    """设置筛选关键词"""
    user = User.objects.get(username=request.user.username)
    if request.POST.get('definekey'):
        key = request.POST.get('definekey').split(',')
        for k in key:
            try:
                KeyName.objects.get(keyname=k.strip())
                continue
            except:
                KeyName.objects.create(user=user,keyname=k.strip())
        return redirect('/file/cve/')
    else:
        return redirect('/file/cve/')

@login_required
def delete_key(request):
    """删除关键词"""
    user = User.objects.get(username=request.user.username)
    key = request.GET.get('key')
    KeyName.objects.filter(user=user, keyname=key.strip()).delete()
    return redirect('/file/cve/')
