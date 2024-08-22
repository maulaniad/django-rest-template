from celery.schedules import crontab


BEAT_SCHEDULE = {
    "hello": {
        "task": "tasks.task_hello.hello",
        "schedule": crontab(minute="*"),
    },
}
