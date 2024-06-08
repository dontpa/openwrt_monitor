from django.contrib import admin
from .models import Heartbeat

# Register your models here.


@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'cpu_usage', 'mem_usage', 'temperature', 'vpn_status')
    list_filter = ('timestamp',)
