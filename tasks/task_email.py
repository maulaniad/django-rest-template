from celery import Task, shared_task

from django.core.mail import send_mail


Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls) # type: ignore[attr-defined]

@shared_task(bind=True)
def task_send_email(self: Task, subject: str, body: str, from_email: str | None, to: list[str], fail_silently: bool = False):
    self.update_state(state="RUNNING", meta={})

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=to,
            fail_silently=fail_silently
        )
    except Exception as e:
        self.update_state(state="FAILURE", meta={'exc': str(e)})
        return False

    self.update_state(state="SUCCESS", meta={})
    return True
