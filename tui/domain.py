import re
from typing import Optional

from .menu import is_alphanumeric
from valid8 import validate
from typeguard import typechecked
from dataclasses import dataclass
from datetime import datetime


def is_alphanumeric(value: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9]*", value))


def is_strong_password(value: str) -> bool:
    pattern = r"^(?=.*[A-Z])" r"(?=.*\d)" r"(?=.*[^a-zA-Z0-9])" r".{8,50}$"
    return bool(re.fullmatch(pattern, value))


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
            min_length=1,
            max_length=50,
            custom=is_alphanumeric,
        )

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Password:

    value: str

    def __post_init__(self):
        validate(
            "Password.value",
            self.value,
            min_length=8,
            max_length=50,
            custom=is_strong_password,
        )


@typechecked
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        validate(
            "Email.value", self.value, min_length=5, max_length=50, custom=is_email
        )


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

