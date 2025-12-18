import pytest
from datetime import datetime, timedelta

from tui.validators import (
    is_valid_password,
    is_email,
    validate_url,
    validate_label,
    validate_private,
    validate_expired_at,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", True),
        ("123", False),
    ],
)
def test_is_valid_password(value, expected):
    assert is_valid_password(value) is expected


def test_is_email_ok():
    assert is_email("test@example.com") is True


def test_is_email_ko():
    with pytest.raises(ValueError, match="Invalid email format"):
        is_email("test@")


def test_validate_url_ok():
    assert validate_url("https://example.com") == "https://example.com"


@pytest.mark.parametrize(
    "url, msg",
    [
        ("", "URL cannot be empty"),
        ("ftp://example.com", "URL must start with http:// or https://"),
        ("http:///path", "URL must have a valid domain"),
    ],
)
def test_validate_url_errors(url, msg):
    with pytest.raises(ValueError, match=msg):
        validate_url(url)


def test_validate_label_ok():
    assert validate_label("ok") == "ok"


@pytest.mark.parametrize(
    "label, msg",
    [
        ("", "Label cannot be empty"),
        ("a" * 101, "Label cannot be longer than 100 characters"),
    ],
)
def test_validate_label_errors(label, msg):
    with pytest.raises(ValueError, match=msg):
        validate_label(label)


def test_validate_private_ok():
    assert validate_private(True) is True


def test_validate_private_ko():
    with pytest.raises(ValueError, match="Private must be a boolean value"):
        validate_private("true")


def test_validate_expired_at_none_ok():
    assert validate_expired_at(None) is None


def test_validate_expired_at_wrong_type():
    with pytest.raises(
        ValueError, match="Expired_at must be a datetime object or None"
    ):
        validate_expired_at("2025-01-01")


def test_validate_expired_at_past():
    past = datetime.now() - timedelta(seconds=1)
    with pytest.raises(ValueError, match="Expiration date must be in the future"):
        validate_expired_at(past)


def test_validate_expired_at_future_ok():
    future = datetime.now() + timedelta(days=1)
    assert validate_expired_at(future) == future
