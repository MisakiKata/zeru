from django.contrib import admin
from apps.logcat import models
# Register your models here.


@admin.register(models.System_info)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname','cpu_brand', 'physical_memory')
    list_per_page = 50

@admin.register(models.Memory_info)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname','memory_total', 'memory_free')
    list_per_page = 50


@admin.register(models.OS_version)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname','version', 'arguments')
    list_per_page = 50


@admin.register(models.Log_user)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('id','hostname', 'uid', 'username','description','directory')
    list_per_page = 50


@admin.register(models.Processes)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'pid', 'name','cmdline')
    list_per_page = 50


@admin.register(models.Crontab)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'command', 'path')
    list_per_page = 50


@admin.register(models.Hidden)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'path', 'filename')
    list_per_page = 50


@admin.register(models.Shell_TTY)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'name', 'path')
    list_per_page = 50


@admin.register(models.Open_Port)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'name', 'path','port','address')
    list_per_page = 50


@admin.register(models.Bean_shell)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'name', 'path','remote_address','remote_port','parent_cmdline')
    list_per_page = 50

