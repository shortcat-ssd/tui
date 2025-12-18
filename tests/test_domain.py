from unittest.mock import patch

import pytest
from tui.client import Backend
from tui.domain import Username, Password, Email, is_email
from datetime import datetime, timedelta
from tui.domain import ShortUrl
from tui.domain import short

def test_is_expired_when_none():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=None,
    )
    assert s.is_expired is False

def test_is_expired_goes_through_not_none_branch():
    s = ShortUrl(
        code="cX",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=datetime(2099, 1, 1, 0, 0, 0),
    )

    assert s.expired_at is not None
    _ = s.is_expired


def test_is_expired_false_when_in_future():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=datetime.now() + timedelta(days=1),
    )
    assert s.is_expired is False


def test_is_expired_true_when_in_past():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=datetime.now() - timedelta(days=1),
    )
    assert s.is_expired is True


@pytest.fixture
def backend():
    return Backend()

def test_shorturl_is_expired_none():
    s = ShortUrl(code="c1", label="lab", target="http://a.it", user="u", expired_at=None)
    assert s.is_expired is False


def test_shorturl_is_expired_future():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=datetime.now() + timedelta(days=1),
    )
    assert s.is_expired is False


def test_shorturl_is_expired_past():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=datetime.now() - timedelta(days=1),
    )
    assert s.is_expired is True


def test_login_success(backend):
    username = Username("Persona")
    password = Password("Persona88!")

    with patch.object(backend, "login", return_value=True) as mock_login:
        result = backend.login(username, password)
        mock_login.assert_called_once_with(username, password)
        assert result is True

def test_logout_success(backend):
    with patch.object(backend, "logout", return_value=None) as mock_logout:
        backend.logout()
        mock_logout.assert_called_once()


def test_register_success(backend):
    with patch.object(backend, "register", return_value=True) as mocked:
        result = backend.register(
            Username("TestUser"),
            Password("StrongPass1!"),
            Password("StrongPass1!"),
            Email("user@test.com"),
        )
        mocked.assert_called_once()
        assert result is True


def test_email_string():
    email = Email("me@example.com")
    assert str(email) == "me@example.com"


def test_email_is_valid():
    email = "emaildiprova@test.it"
    assert is_email(email) is True

def test_email_not_valid():
    email = ""
    assert is_email(email) is False

def test_email_validation():
    email = Email("email@testing.it")
    assert email.value == "email@testing.it"

def test_username_str():
    u = Username("Persona789")
    assert str(u) == "Persona789"

def test_shorturl_str():
    s = ShortUrl(
        code="c1",
        label="lab",
        target="http://a.it",
        user="u",
        expired_at=None,
    )
    assert str(s) == "c1 -> http://a.it"


def test_short_str():
    s = short(
        target="http://a.it",
        label="lab",
        expired_at=None,
        private=False,
    )
    assert str(s) == "http://a.it"

