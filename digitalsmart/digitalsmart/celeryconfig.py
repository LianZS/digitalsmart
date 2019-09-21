import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digitalsmart.settings')  # 将celery加载到全局-----非常重要的一步

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"
# 添加需要加载的任务模块
CELERY_IMPORTS = ("datainterface.tasks", "datainterface.analyse",)
# 生成任务队列
CELERY_QUEUES = (
    Queue('distribution', routing_key='datainterface.tasks.#', exchange=Exchange('tasks', type='direct')),
    Queue('word', routing_key='datainterface.analyse.#', exchange=Exchange('analy', type='direct')),

)
# 任务路由器
CELERY_ROUTES = {
    "datainterface.tasks.#": {'queue': "distribution"},
    "datainterface.analyse.#": {'queue': "word"},

}
CELERYD_CONCURRENCY = 10  # 设置并发的worker数量

CELERYD_MAX_TASKS_PER_CHILD = 150  # 每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERY_TASK_ACKS_LATE = True  # 允许重试
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
app = Celery("celery")
