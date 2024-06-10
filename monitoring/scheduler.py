# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.core.management import call_command
from django.db import transaction
import threading
import logging

# 设置日志记录
logger = logging.getLogger(__name__)

# 单例模式
_scheduler = None
_scheduler_lock = threading.Lock()


def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.add_jobstore(DjangoJobStore(), "default")
        register_events(_scheduler)
    return _scheduler


def check_heartbeat_job():
    call_command("check_heartbeat")


@transaction.atomic
def start_scheduler():
    global _scheduler_lock
    with _scheduler_lock:
        scheduler = get_scheduler()
        scheduler.add_job(
            "monitoring.scheduler:check_heartbeat_job",
            "interval",
            hours=2.5,  # 调试时使用30秒，实际应用中改为hours=2.5
            id="check_heartbeat",
            replace_existing=True,
        )
        if not scheduler.running:
            scheduler.start()
            print("Scheduler started!")
        else:
            print("Scheduler is already running!")


# 停止调度器时关闭所有任务
def stop_scheduler():
    scheduler = get_scheduler()
    try:
        if scheduler.running:
            scheduler.shutdown()
            print("Scheduler stopped!")
        else:
            print("Scheduler is not running!")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
