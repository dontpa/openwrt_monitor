# your_app_name/management/commands/check_heartbeat.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import requests
from monitoring.models import Heartbeat

WEBHOOK_URL = '你的飞书webhook URL'

class Command(BaseCommand):
    help = "Check heartbeat and VPN status."

    def handle(self, *args, **options):
        now = timezone.now()
        threshold_time = now - timedelta(hours=2.5)
        recent_heartbeat = Heartbeat.objects.filter(
            timestamp__gte=threshold_time
        ).last()

        print("heartbeat checking")
        if not recent_heartbeat:
            # 2.5小时内没有收到心跳包
            message = {"msg_type": "text", "content": {"text": "路由器未正常工作"}}
            requests.post(WEBHOOK_URL, json=message)
        elif not recent_heartbeat.vpn_status:
            # VPN 状态为 false
            message = {"msg_type": "text", "content": {"text": "VPN未正常工作"}}
            requests.post(WEBHOOK_URL, json=message)
