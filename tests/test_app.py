from unittest.mock import patch

from tui.app import do_login, do_register, logout, edit_password, convert_url


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