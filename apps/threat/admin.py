from django.contrib import admin
from apps.threat.models import FileMonitor, CVESerach, KeyName
# Register your models here.

@admin.register(FileMonitor)
class FileAdmin(admin.ModelAdmin):
    list_display = ('action', 'mtime', 'target_path', 'uid', 'mode')
    list_per_page = 50


@admin.register(CVESerach)
class CVEAdmin(admin.ModelAdmin):
    list_display = ('id', 'cve', 'summary', 'time')
    list_per_page = 50

@admin.register(KeyName)
class CVEAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'keyname')
    list_per_page = 50