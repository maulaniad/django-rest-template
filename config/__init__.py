# Import objects if needed in settings.py to avoid circular import error
from helpers.response import ResponseRenderer    # noqa: F401


# Setup celery app for celery_beat
from config.celery import app as celery_app

__all__ = ["celery_app"]
