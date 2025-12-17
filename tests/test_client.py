# tests/test_client.py
from unittest.mock import Mock
from datetime import datetime

import pytest

from tui.client import Backend, BASE_URL
from tui.domain import Username, Password, Email, ShortUrl, short


@pytest.fixture
def backend():
    b = Backend()
    # session finta (evita HTTP)
    b.session = Mock()
    b.session.cookies = Mock()
    return b


def test_login_success(backend):
    backend.session.post.return_value.ok = True

    u = Username("Persona")
    p = Password("Persona88!")

    result = backend.login(u, p)

    assert result is True
    backend.session.post.assert_called_once_with(
        f"{BASE_URL}/auth/login/",
        data={"username": u.value, "password": p.value},
    )


def test_login_fail(backend):
    backend.session.post.return_value.ok = False

    u = Username("Persona")
    p = Password("Persona88!")

    result = backend.login(u, p)

    assert result is False


def test_logout_success_clears_cookies(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.post.return_value.ok = True

    backend.logout()

    backend.session.post.assert_called_once_with(
        f"{BASE_URL}/auth/logout/",
        headers={"X-CSRFToken": "csrf123"},
    )
    backend.session.cookies.clear.assert_called_once()


def test_logout_fail_does_not_clear_cookies(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.post.return_value.ok = False

    backend.logout()

    backend.session.cookies.clear.assert_not_called()


def test_register_success(backend):
    backend.session.post.return_value.ok = True

    result = backend.register(
        Username("TestUser"),
        Password("StrongPass1!"),
        Password("StrongPass1!"),
        Email("user@test.com"),
    )

    assert result is True
    backend.session.post.assert_called_once()


def test_register_fail(backend):
    resp = backend.session.post.return_value
    resp.ok = False
    resp.status_code = 400
    resp.text = "bad request"

    result = backend.register(
        Username("TestUser"),
        Password("StrongPass1!"),
        Password("StrongPass1!"),
        Email("user@test.com"),
    )

    assert result is False


def test_edit_password_new_passwords_do_not_match(backend):
    ok, msg = backend.edit_password("OldPass1!", "NewPass1!", "Different1!")
    assert ok is False
    assert msg == "New passwords do not match"
    backend.session.post.assert_not_called()


def test_edit_password_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.post.return_value.ok = True

    ok, msg = backend.edit_password("OldPass1!", "NewPass1!", "NewPass1!")

    assert ok is True
    assert msg == "Password changed successfully"
    backend.session.post.assert_called_once_with(
        f"{BASE_URL}/auth/password/change/",
        json={
            "old_password": "OldPass1!",
            "new_password1": "NewPass1!",
            "new_password2": "NewPass1!",
        },
        headers={"X-CSRFToken": "csrf123"},
    )


def test_edit_target(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = True

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    assert backend.edit_target(s, "http://b.it") is True

    backend.session.patch.assert_called_once_with(
        f"{BASE_URL}/shorts/{s.code}/",
        json={"target": "http://b.it"},
        headers={"X-CSRFToken": "csrf123"},
    )


def test_edit_expire_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = True

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    dt = datetime(2030, 1, 1, 12, 0, 0)

    ok, msg = backend.edit_expire(s, dt)

    assert ok is True
    assert msg == "Expiry updated successfully"


def test_edit_visibility_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = True

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_visibility(s, True)

    assert ok is True
    assert msg == "Visibility changed successfully"


def test_delete_url_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.delete.return_value.ok = True

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.deleteUrl(s)

    assert ok is True
    assert msg == "URL deleted successfully."


def test_get_short_url_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.get.return_value.ok = True
    backend.session.get.return_value.json.return_value = [
        {"code": "c1", "target": "http://a.it", "label": "A", "private": False, "expired_at": None},
        {"code": "c2", "target": "http://b.it", "label": "B", "private": True, "expired_at": None},
    ]

    ok, urls = backend.getShortUrl()

    assert ok is True
    assert len(urls) == 2
    assert urls[0].code == "c1"
    assert urls[1].private is True
