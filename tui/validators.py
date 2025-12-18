import re
from datetime import datetime
from urllib.parse import urlparse
from typing import Callable, Optional

from typeguard import typechecked
from valid8 import ValidationError


@typechecked
def pattern(pattern: str) -> Callable[[str], bool]:
    def validator(value: str) -> bool:
        return bool(re.fullmatch(pattern, value))

    validator.__name__ = f"pattern ({pattern})"

    return validator


@typechecked
def is_valid_password(value: str) -> bool:
    return not value.isdigit()


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
