import re
from urllib.parse import urlparse
from valid8 import ValidationError
from typing import Optional
from datetime import datetime


def is_alphanumeric(value: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9]*", value))


def is_strong_password(value: str) -> bool:

    if not value:
        raise ValidationError("Password cannot be empty")
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if len(value) > 128:  # limite simile a Django
        raise ValidationError("Password cannot be longer than 128 characters")
    return True


def is_email(value: str) -> bool:

    pattern = r"^[a-z0-9._-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$"
    if not re.fullmatch(pattern, value):
        raise ValidationError("Invalid email format")
    return True


def validate_url(url: str) -> str:
    if not url:
        raise ValidationError("URL cannot be empty")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError("URL must start with http:// or https://")
    if not parsed.netloc:
        raise ValidationError("URL must have a valid domain")
    return url


def validate_label(label: str) -> str:
    if not label:
        raise ValidationError("Label cannot be empty")
    if len(label) > 100:
        raise ValidationError("Label cannot be longer than 100 characters")
    return label


def validate_private(private) -> bool:
    if not isinstance(private, bool):
        raise ValidationError("Private must be a boolean value")
    return private


def validate_expired_at(expired_at: Optional[datetime]) -> Optional[datetime]:
    if expired_at is not None:
        if not isinstance(expired_at, datetime):
            raise ValidationError("Expired_at must be a datetime object or None")
        if expired_at <= datetime.now():
            raise ValidationError("Expiration date must be in the future")
    return expired_at
