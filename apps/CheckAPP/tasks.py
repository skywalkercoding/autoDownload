import atexit
import time

from django_apscheduler.jobstores import DjangoJobStore

from apps.CheckAPP.Base.HandleExcel.BaseView import BaseView
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
executors = {
        'default': {
            'type': 'threadpool',
            'max_workers': 20
        }
    }
scheduler.configure(executors=executors)
is_scheduler_running = False  # 新增标志位


def google_version_task():
    try:
         print("Running scheduled task...")
    # 任务逻辑

         basView=BaseView()
         basView.daily_task_run()
         print("Task completed.")
    except Exception as e:
        print(f"Error in google_version_task: {e}")

def cleanup_old_jobs():
    # 清理过期的任务记录
    DjangoJobExecution.objects.delete_old_job_executions(max_age=604800)  # 删除一周前的记录

def start_scheduler():

    trigger = CronTrigger(hour=10, minute=20)

    # trigger = IntervalTrigger(seconds=60)
    scheduler.add_job(google_version_task, trigger=trigger)
    try:
        # 启动调度程序
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # 当通过键盘中断或系统退出时停止调度程序
        scheduler.shutdown()

    # 设置标志位为 True

