import logging
import osquery,json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import socket

def System_info():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select * from system_info;")
    HeaderMess('System_info', ret.response)


def OS_version():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select * from os_version;")
    HeaderMess('OS_version', ret.response)


def Memory_info():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select * from memory_info;")
    HeaderMess('Memory_info', ret.response)


def Log_user():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select uid,gid,username,description,directory,shell from users;")
    if not ret.response:
        return
    HeaderMess('Log_user', ret.response)


def Processes():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select pid,name,path,cmdline from processes;")
    if not ret.response:
        return
    HeaderMess('Processes', ret.response)


def Crontab():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select * from crontab;")
    if not ret.response:
        return
    HeaderMess('Crontab', ret.response)


def Hidden():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("SELECT hash.sha1, fi.path, fi.filename, datetime(fi.btime, 'unixepoch', 'UTC') as btime, datetime(fi.atime, 'unixepoch', 'UTC') as atime, datetime(fi.ctime, 'unixepoch', 'UTC') as ctime, datetime(fi.mtime, 'unixepoch', 'UTC') as mtime FROM hash JOIN file fi USING (path) where ((fi.path like '/home/%%/.%') OR (fi.path like '/root/.%')) AND type='regular';")
    if not ret.response:
        return
    HeaderMess('Hidden', ret.response)


def Shell_TTY():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select DISTINCT p.name, p.path, pos.remote_address, pos.remote_port from process_open_sockets pos LEFT JOIN processes p ON pos.pid = p.pid WHERE pos.remote_port != 0 AND p.name != '';")
    if not ret.response:
        return
    HeaderMess('Shell_TTY', ret.response)


def Open_Port():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("select p.name, p.path, lp.port, lp.address,lp.pid  from listening_ports lp LEFT JOIN processes p ON lp.pid = p.pid WHERE lp.port != 0 AND p.name != '';")
    if not ret.response:
        return
    HeaderMess('Open_Port', ret.response)


def Bean_shell():
    instance = osquery.SpawnInstance()
    instance.open()
    ret = instance.client.query("SELECT DISTINCT(processes.pid), processes.name,processes.path, processes.cmdline, processes.root,process_open_sockets.remote_address,process_open_sockets.remote_port, (SELECT cmdline FROM processes AS parent_cmdline WHERE pid=processes.parent) AS parent_cmdline FROM processes JOIN process_open_sockets USING (pid) LEFT OUTER JOIN process_open_files ON processes.pid = process_open_files.pid WHERE remote_address NOT IN ('0.0.0.0','::','') and name in ('sh','bash','nc') AND remote_address NOT LIKE '10.%' AND remote_address NOT LIKE '192.168.%';")
    if not ret.response:
        return
    HeaderMess('Bean_shell', ret.response)


def HeaderMess(topic, data):
    for d in data:
        if Host != '':
            d['hostip'] = Host
        else:
            d['hostip'] = get_host_ip()
        SendMess(topic, d)

def SendMess(topic, messgae):
    producer = KafkaProducer(
        bootstrap_servers=Kafka_Host,
        value_serializer=lambda m: json.dumps(m).encode('ascii')
    )
    future = producer.send(topic, messgae)
    try:
        future.get(timeout=10)
    except KafkaError as e:
        logging.basicConfig(level=logging.warning(e),
                            filename='zeru.log',
                            filemode='a',
                            format=
                            '%(asctime)s - %(pathname)s - %(levelname)s: %(message)s')


def get_host_ip():
    s = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def Filemonitor():
    input = open(osquery_log)
    for line in input.readlines():
        line = json.loads(line)
        if line['name'] == 'file_events':
            if Host != '':
                line['hostip'] = Host
            else:
                line['hostip'] = get_host_ip()
            SendMess('Filemonitor', line)
    input.close()


def main():
    System_info()
    OS_version()
    Memory_info()
    Log_user()
    Processes()
    Crontab()
    Hidden()
    Shell_TTY()
    Open_Port()
    Bean_shell()
    Filemonitor()


if __name__ == '__main__':
    Kafka_Host = ['']             #kafka地址
    Host = ''                   #主机IP
    osquery_log = '/var/log/osquery/osqueryd.results.log'            #osquery log  注意权限
    main()