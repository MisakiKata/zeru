from django.urls import path
from apps.logcat import views


app_name = 'logcat'

extra_urlpatter = [
    path('system/', views.system, name='system'),
    path('version/', views.version, name='version'),
    path('memory/', views.memory, name='memory'),
    path('user/', views.user, name='user'),
    path('processes/', views.processes, name='processes'),
    path('crontab/', views.crontab, name='crontab'),
    path('hidden/', views.hidden, name='hidden'),
    path('shell/', views.shell_tty, name='shell'),
    path('port/', views.open_port, name='port'),
    path('bean/', views.bean_shell, name='bean'),
]