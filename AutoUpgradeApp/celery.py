# myproject/celery.py

from __future__ import absolute_import, unicode_literals

import logging
import os
from celery import Celery
from celery.signals import setup_logging

# 设置 Django 的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoUpgradeApp.settings')

# 创建 Celery 实例
app = Celery('AutoUpgradeApp')

# 使用 Django 配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有注册的 Django app 配置中加载任务模块
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwags):
    logging.getLogger('celery').setLevel(logging.DEBUG)