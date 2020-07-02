from django.contrib import admin
from apps.host.models import Host, Kafka
# Register your models here.


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('Auther', 'Hostname', 'Email', 'Active')
    list_per_page = 50

@admin.register(Kafka)
class KafkaAdmin(admin.ModelAdmin):
    list_display = ('Kafka', 'Active')
    list_per_page = 50