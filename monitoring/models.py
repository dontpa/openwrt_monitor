from django.db import models

# Create your models here.
class Heartbeat(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    mem_usage = models.FloatField()
    temperature = models.FloatField()
    vpn_status = models.BooleanField()