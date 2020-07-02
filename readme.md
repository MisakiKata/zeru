### 又叒叒一个基于osquery的监控

此项目是基于osquery的数据收集分析项目，用来监控主机，从最初的学习项目到现在的具有一定使用价值的项目。

数据流使用kafka来传输，客户端定时收集发送，服务的定时拉取，所以并没有实时监控。

基于osquery的项目官方有很多推荐，至于自己写一方面是为了学习django，一方面是为了二次开发。如果需要更完善和美观的项目可以采用官方的推荐。

#### osquery配置

以下配置只是用来表示文件监控的一部分，至于其他的配置并没有使用。`/etc/osquery/osquery.conf`

```
{
	"options": {
	"config_plugin":"filesystem",
        "logger_plugin":"filesystem",
        "logger_path":"/var/log/osquery",
        "disable_logging":"false",
        "schedule_splay_percent":"10",
        "verbose":"false",
        "pidfile":"/var/osquery/osquery.pidfile",
        "enable_syslog": "true",
	"worker_threads":"5",
	"host_identifier":"hostname",
        "disable_events":"false",
        "disable_audit":"false",
        "audit_allow_config":"true",
        "audit_allow_sockets":"true"
	},
	"file_paths": {
		"html": [
			"/var/www/%%"
		]
	},
	"schedule": {
		"file_events": {
			"query": "SELECT * FROM file_events;",
			"removed": false,
			"interval": 600
		}
	}
}
```

#### kafka

配置根据官方推荐来即可，如果不在同一台主机，需要注意跨主机访问的配置。

#### 配置

默认django的非debug模式，需要开启监控，到设置中上面的选择开启即可。如果有问题可以先关闭再调试。agent目录为客户端文件，定时运行即可。默认定时为十分钟拉取一次，需要修改到`apps/threat/views.py`修改即可。

需要主机的IP做处理，所以最好先定义agent中的IP地址。如果不定义会自己识别，但不一定正确。

系统信息中会显示全部存在的信息，为了避免大量数据加载，所以只默认显示最近七天的数据。如果需要修改时间，可以到`apps/logcat/views.py`中修改。

#### 截图

![image-20200702135628638](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200702135635.png)

![image-20200702140400754](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200702140400.png)
