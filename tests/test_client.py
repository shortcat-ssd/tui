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

def test_edit_password_fail_returns_json(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.post.return_value
    resp.ok = False
    resp.json.return_value = {"detail": "err"}

    ok, msg = backend.edit_password("OldPass1!", "NewPass1!", "NewPass1!")
    assert ok is False
    assert msg == {"detail": "err"}


def test_edit_password_fail_returns_text_when_json_raises(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.post.return_value
    resp.ok = False
    resp.json.side_effect = Exception("no json")
    resp.text = "server error"

    ok, msg = backend.edit_password("OldPass1!", "NewPass1!", "NewPass1!")
    assert ok is False
    assert msg == "server error"

def test_edit_expire_fail_status_text(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.patch.return_value
    resp.ok = False
    resp.status_code = 500
    resp.text = "boom"

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_expire(s, datetime(2030, 1, 1, 12, 0, 0))
    assert ok is False
    assert "500" in msg

def test_edit_username_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = True

    ok, msg = backend.edit_username(Username("NewUser99"))

    assert ok is True
    assert msg == "Username changed successfully"
    backend.session.patch.assert_called_once_with(
        f"{BASE_URL}/auth/user/",
        json={"username": Username("NewUser99")},
        headers={"X-CSRFToken": "csrf123"},
    )


def test_edit_expire_exception(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.side_effect = Exception("timeout")

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_expire(s, datetime(2030, 1, 1, 12, 0, 0))
    assert ok is False
    assert "timeout" in msg


def test_edit_visibility_fail(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = False
    backend.session.patch.return_value.text = "nope"

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_visibility(s, False)

    assert ok is False
    assert msg == "nope"


def test_edit_username_fail_returns_json(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.patch.return_value
    resp.ok = False
    resp.json.return_value = {"username": ["error"]}

    ok, msg = backend.edit_username(Username("NewUser99"))
    assert ok is False
    assert msg == {"username": ["error"]}


def test_edit_username_fail_returns_text_when_json_raises(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.patch.return_value
    resp.ok = False
    resp.json.side_effect = Exception("no json")
    resp.text = "bad"

    ok, msg = backend.edit_username(Username("NewUser99"))
    assert ok is False
    assert msg == "bad"

def test_create_url_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.post.return_value
    resp.ok = True
    resp.json.return_value = {"code": "zzz"}

    s = short(target="http://a.it", label="lab", expired_at=None, private=False)
    ok, out = backend.createUrl(s)

    assert ok is True
    assert out == "http://localhost:8000/zzz"


def test_create_url_fail(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.post.return_value
    resp.ok = False
    resp.status_code = 400
    resp.text = "bad request"

    s = short(target="http://a.it", label="lab", expired_at=None, private=False)
    ok, out = backend.createUrl(s)

    assert ok is False
    assert "400" in out


def test_create_url_exception(backend):
    backend.session.post.side_effect = Exception("network down")

    s = short(target="http://a.it", label="lab", expired_at=None, private=False)
    ok, out = backend.createUrl(s)

    assert ok is False
    assert "network down" in out

def test_delete_url_fail(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.delete.return_value
    resp.ok = False
    resp.status_code = 404
    resp.text = "not found"

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, out = backend.deleteUrl(s)

    assert ok is False
    assert "404" in out


def test_delete_url_exception(backend):
    backend.session.delete.side_effect = Exception("boom")

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, out = backend.deleteUrl(s)

    assert ok is False
    assert "boom" in out

def test_get_short_url_fail(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.get.return_value
    resp.ok = False
    resp.status_code = 403
    resp.text = "forbidden"

    ok, out = backend.getShortUrl()
    assert ok is False
    assert "403" in out


def test_get_short_url_exception(backend):
    backend.session.get.side_effect = Exception("timeout")

    ok, out = backend.getShortUrl()
    assert ok is False
    assert "timeout" in out

def test_get_short_url_success_with_patched_shorturl(backend, monkeypatch):
    import tui.client as client_mod

    class DummyShortUrl:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    monkeypatch.setattr(client_mod, "ShortUrl", DummyShortUrl)

    backend.session.cookies.get.return_value = "csrf123"
    backend.session.get.return_value.ok = True
    backend.session.get.return_value.json.return_value = [
        {"code": "c1", "target": "http://a.it", "label": "A", "private": False, "expired_at": None},
    ]

    ok, urls = backend.getShortUrl()
    assert ok is True
    assert urls[0].code == "c1"

def test_edit_label_success(backend):
    backend.session.cookies.get.return_value = "csrf123"
    backend.session.patch.return_value.ok = True

    class Dummy:
        code = "abc123"

    ok, msg = backend.edit_label("NEWLABEL", Dummy())

    assert ok is True
    assert msg == "Label changed successfully"


def test_edit_expire_fail_branch(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.patch.return_value
    resp.ok = False
    resp.status_code = 500
    resp.text = "boom"

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_expire(s, datetime(2030, 1, 1, 12, 0, 0))

    assert ok is False
    assert msg == "500: boom"


def test_edit_expire_exception_branch(backend):
    backend.session.patch.side_effect = Exception("timeout")

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.edit_expire(s, datetime(2030, 1, 1, 12, 0, 0))

    assert ok is False
    assert msg == "timeout"



def test_edit_label_fail_branch(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.patch.return_value
    resp.ok = False
    resp.status_code = 400
    resp.text = "bad request"

    class Dummy:
        code = "abc123"

    ok, msg = backend.edit_label("NEW", Dummy())

    assert ok is False
    assert msg == "400: bad request"


def test_edit_label_exception_branch(backend):
    backend.session.patch.side_effect = Exception("network down")

    class Dummy:
        code = "abc123"

    ok, msg = backend.edit_label("NEW", Dummy())

    assert ok is False
    assert msg == "network down"



def test_create_url_fail_branch(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.post.return_value
    resp.ok = False
    resp.status_code = 400
    resp.text = "bad request"

    s = short(target="http://a.it", label="lab", expired_at=None, private=False)
    ok, msg = backend.createUrl(s)

    assert ok is False
    assert msg == "400: bad request"


def test_create_url_exception_branch(backend):
    backend.session.post.side_effect = Exception("boom")

    s = short(target="http://a.it", label="lab", expired_at=None, private=False)
    ok, msg = backend.createUrl(s)

    assert ok is False
    assert msg == "boom"


def test_delete_url_fail_branch(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.delete.return_value
    resp.ok = False
    resp.status_code = 404
    resp.text = "not found"

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.deleteUrl(s)

    assert ok is False
    assert msg == "404: not found"


def test_delete_url_exception_branch(backend):
    backend.session.delete.side_effect = Exception("kaboom")

    s = ShortUrl(code="abc123", label="x", target="http://a.it", user="u")
    ok, msg = backend.deleteUrl(s)

    assert ok is False
    assert msg == "kaboom"



def test_get_short_url_fail_branch(backend):
    backend.session.cookies.get.return_value = "csrf123"
    resp = backend.session.get.return_value
    resp.ok = False
    resp.status_code = 403
    resp.text = "forbidden"

    ok, msg = backend.getShortUrl()

    assert ok is False
    assert msg == "403: forbidden"


def test_get_short_url_exception_branch(backend):
    backend.session.get.side_effect = Exception("timeout")

    ok, msg = backend.getShortUrl()

    assert ok is False
    assert msg == "timeout"