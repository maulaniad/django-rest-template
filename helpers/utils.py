from fastnanoid import generate
from jwt import encode
from random import randint
from typing import Any

from django.conf import settings
from django.utils.timezone import now, timedelta

from rest_framework.utils.serializer_helpers import ReturnDict

from helpers.types import EmailMessage
from tasks.task_email import task_send_email


def generate_oid(length: int = 21):
    """Generates unique value with NanoID of given length."""
    return generate(size=length)


def generate_token(data: dict[str, Any] | ReturnDict[str, Any]):
    """Generates JWT token with given data."""
    time = now()

    encoded_token = encode(
        {
            **data,
            'exp': (time + timedelta(hours=settings.JWT_EXP_HOURS)).timestamp(),
            'iat': time.timestamp()
        },
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_token


def generate_otp():
    """Generates OTP with given length."""
    return randint(100000, 999999)


def send_email(email: EmailMessage, fail_silently: bool = False):
    """Customized function to send an email, asynchronously."""
    task_send_email.delay(
        subject=email.subject,
        body=email.body,
        from_email=email.from_email,
        to=email.to,
        fail_silently=fail_silently
    )
