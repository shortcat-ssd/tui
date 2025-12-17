from unittest.mock import patch, MagicMock

from tui.app import do_login, do_register, logout, edit_password, convert_url, edit_url, delete_url

from tui.domain import short



@patch('tui.app.submenu')
@patch('tui.app.client')
@patch('builtins.input', side_effect=['Utente'])
@patch('tui.app.getpass', return_value='Persona00!')
def test_do_login_success(mock_input, mock_getpass, mock_client, mock_submenu):
    mock_client.login.return_value = True

    do_login()

    mock_client.login.assert_called_once()
    mock_submenu.assert_called_once()



@patch('tui.app.submenu')
@patch('tui.app.client')
@patch('builtins.input', side_effect=["NuovoUtente", "nuovoutente@email.it"])
@patch('tui.app.getpass', side_effect=['Persona00!', 'Persona00!'])
def test_do_register_success(mock_input, mock_getpass, mock_client, mock_submenu):
    mock_client.register.return_value = True
    mock_client.login.return_value = True

    try:
        do_register()
    except KeyboardInterrupt:
        pass

    mock_client.register.assert_called_once()
    mock_client.login.assert_called_once()
    mock_submenu.assert_called_once()



@patch('tui.app.submenu')
@patch('tui.app.client')
@patch('tui.app.getpass', return_value='Persona00!')
@patch('builtins.input', side_effect=['Utente', KeyboardInterrupt])
def test_do_login_fail(mock_input, mock_getpass, mock_client, mock_submenu):
    mock_client.register.side_effect = [False, KeyboardInterrupt]
    mock_client.login.side_effect = [False, KeyboardInterrupt]

    try:
        do_login()
    except KeyboardInterrupt:
        pass
    mock_client.login.assert_called_once()
    mock_submenu.assert_not_called()



@patch('tui.app.client')
def test_logout_success(mock_client):
    mock_client.logout.return_value = True

    logout()
    mock_client.logout.assert_called_once()


@patch('tui.app.submenu')
@patch('tui.app.client')
@patch('builtins.print')
@patch('builtins.input', side_effect=['Utente', 'utente@email.it', KeyboardInterrupt])
@patch('tui.app.getpass', side_effect=['Password1!', 'Password2!', KeyboardInterrupt])

def test_do_register_passwords_do_not_match(
    mock_getpass,
    mock_input,
    mock_print,
    mock_client,
    mock_submenu
):
    try:
        do_register()
    except KeyboardInterrupt:
        pass


    mock_client.register.assert_not_called()
    mock_client.login.assert_not_called()
    mock_submenu.assert_not_called()


    assert any(
        "Passwords do not match" in str(call)
        for call in mock_print.call_args_list
    )

@patch('tui.app.client')
@patch('builtins.print')
@patch('builtins.input', side_effect=['https://chatgpt.com/c/69431ef9-3d90-832c-8603-8df5895a1544', 'label','2026-09-09 09:09', "yes", KeyboardInterrupt])
def test_convert_url_success(mock_input, mock_print, mock_client):
    mock_client.createUrl.return_value = (True, "http://short.url/abc123")

    convert_url()

    assert mock_client.createUrl.called

    assert any(
        "Short URL created" in str(call_arg)
        for call_arg in mock_print.call_args_list
    )

    short_obj_passed = mock_client.createUrl.call_args[0][0]
    assert isinstance(short_obj_passed, type(short("", "", "", False)))

class ValidationError(Exception):
    pass

"""
@patch('builtins.input', side_effect=[' ', 'label','2026-09-09 09:09', "yes"])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.validate_url', side_effect=ValidationError("dummy"))
def test_convert_url_fail(mock_validate_url, mock_client, mock_print, mock_input):

    convert_url()


    mock_client.createUrl.assert_not_called()

    assert any("dummy" in str(call) for call in mock_print.call_args_list)
"""


@patch('builtins.input', side_effect=['https://example.com', 'label', '2026-99-99 99:99', 'yes'])
@patch('builtins.print')
@patch('tui.app.client')
def test_convert_url_invalid_date(mock_client, mock_print, mock_input):
    convert_url()

    mock_client.createUrl.assert_not_called()

    printed_messages = [str(call) for call in mock_print.call_args_list]
    assert any("Invalid date format" in msg for msg in printed_messages)


@patch('builtins.input', side_effect=['user1', 'user1@example.com', KeyboardInterrupt])
@patch('tui.app.getpass', side_effect=['Password1!', 'Password1!'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.submenu')
def test_do_register_client_fail(mock_submenu, mock_client, mock_print, mock_getpass, mock_input):

    mock_client.register.return_value = False


    try:
        do_register()
    except KeyboardInterrupt:
        pass

    mock_client.register.assert_called_once()


    mock_client.login.assert_not_called()
    mock_submenu.assert_not_called()


    printed_messages = [str(call) for call in mock_print.call_args_list]
    assert any("Registration failed" in msg for msg in printed_messages)


@patch('tui.app.editmenu')
def test_edit_url_calls_editmenu(mock_editmenu):
    edit_url()

    mock_editmenu.assert_called_once()


@patch('builtins.print')
@patch('tui.app.client')
def test_delete_url_get_shorturl_error(mock_client, mock_print):
    mock_client.getShortUrl.return_value = (False, "Fetch error")
    delete_url()
    mock_print.assert_called_with("Error fetching URLs:", "Fetch error")

@patch('builtins.input', side_effect=['abc'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict', return_value={1: MagicMock(label="label1")})
def test_delete_url_non_numeric(mock_urls_to_dict, mock_show, mock_client, mock_print, mock_input):
    mock_client.getShortUrl.return_value = (True, [MagicMock(label="label1")])
    delete_url()
    mock_print.assert_called_with("Enter valid number.")

@patch('builtins.input', side_effect=['2'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict', return_value={1: MagicMock(label="label1")})
def test_delete_url_invalid_number(mock_urls_to_dict, mock_show, mock_client, mock_print, mock_input):
    mock_client.getShortUrl.return_value = (True, [MagicMock(label="label1")])
    delete_url()
    mock_print.assert_called_with("Invalid number.")
