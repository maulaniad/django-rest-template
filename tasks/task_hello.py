from celery import Task, shared_task


Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls) # type: ignore[attr-defined]

@shared_task(bind=True, ignore_result=True)
def hello(self: Task):
    print("Hello from Celery")
    return {'exc_type': "OK", 'exc_message': "Celery Successfully Run"}
