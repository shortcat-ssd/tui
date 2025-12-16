from unittest.mock import patch

from tui.app import do_login, do_register, logout, edit_password



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


