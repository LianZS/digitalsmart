import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digitalsmart.settings')  # 将celery加载到全局-----非常重要的一步

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"
CELERY_IMPORTS = ("datainterface.tasks",)
CELERY_QUEUES = (
    Queue('distribution', routing_key='datainterface.tasks.#', exchange=Exchange('tasks', type='direct')),

)
CELERY_ROUTES = {
    "datainterface.tasks.#": {'queue': "distribution"},
}
CELERYD_CONCURRENCY = 7  # 设置并发的worker数量

CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERY_TASK_ACKS_LATE = True  # 允许重试
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
app = Celery("celery")
