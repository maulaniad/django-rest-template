from fastnanoid import generate
from jwt import encode
from typing import Any

from django.conf import settings
from django.utils.timezone import now, timedelta

from rest_framework.utils.serializer_helpers import ReturnDict


def generate_oid(length: int = 21):
    """Generates unique value with NanoID of given length."""
    return generate(size=length)


def generate_token(data: dict[str, Any] | ReturnDict[str, Any]):
    """Generates JWT token with given data."""
    time = now()

    encoded_token = encode(
        {
            **data,
            'exp': time + timedelta(hours=settings.JWT_EXP_HOURS, microseconds=time.microsecond),
        },
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_token
