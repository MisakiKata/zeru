from django.urls import path
from apps.threat import views


app_name = 'threat'


extra_urlpatter = [
    path('monitor/', views.filemonitor, name='monitor'),
    path('comshow/', views.Message_save, name='comshow'),
    path('inbox/', views.inbox, name='inbox'),
    path('read/', views.read, name='read'),
    path('cve/', views.cve, name='cve'),
    path('delect/', views.delete_key, name='delete_key'),
    path('add/', views.definekey, name='definekey'),
]