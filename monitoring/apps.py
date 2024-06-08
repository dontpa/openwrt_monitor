from django.apps import AppConfig
import os


class MonitoringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monitoring"

    def ready(self):
        # 仅在主进程中启动调度器
        if os.environ.get("RUN_MAIN", None) != "true":
            from monitoring import scheduler

            scheduler.start_scheduler()
