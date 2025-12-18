import re
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from valid8 import validate
from typeguard import typechecked

from tui.validators import pattern, is_valid_password


def is_email(value: str) -> bool:
    pattern = r"^[a-z0-9._-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$"
    return bool(re.fullmatch(pattern, value))


@typechecked
@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        validate(
            "Username.value",
            self.value,
            min_len=1,
            max_len=150,
            custom=pattern(r"^[\w.@+-]+$"),
            help_msg="Username must be 1-150 characters and contain only letters, numbers, and @./+_-",
        )

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        validate(
            "Password.value",
            self.value,
            min_len=8,
            custom=is_valid_password,
            help_msg="Password must be at least 8 characters long and cannot be entirely numeric",
        )


@typechecked
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        validate(
            "Email.value",
            self.value,
            custom=pattern(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"),
            help_msg="Invalid email format",
        )
    
    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class ShortUrl:
    code: str
    label: str
    target: str
    user: str
    private: bool = False
    expired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        return self.expired_at is not None and self.expired_at <= datetime.now()

    def __str__(self):
        return f"{self.code} -> {self.target}"


@typechecked
@dataclass(frozen=True)
class short:
    target: str
    label: str
    expired_at: Optional[datetime] = None
    private: bool = False

    def __str__(self):
        return f"{self.target}"
