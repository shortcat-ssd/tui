from unittest.mock import patch

import pytest
from tui.client import Backend
from tui.domain import Username, Password, Email, is_email


@pytest.fixture
def backend():
    return Backend()






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

