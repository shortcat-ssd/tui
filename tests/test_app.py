from unittest.mock import patch

from tui.app import do_login, do_register, logout, edit_password, modify_target, modify_label


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


def test_modify_target_success(capsys):
    fake_short_url = "short123"
    fake_new_target = "http://nuovo-sito.com"

    # 1. Mockiamo 'same_method' per restituire uno short_url valido
    with patch('tui.app.same_method', return_value=fake_short_url) as mock_same:
        with patch('tui.app.input', return_value=fake_new_target):
            with patch('tui.app.validate_url', return_value=fake_new_target):
                with patch('tui.app.client.edit_target', return_value=True) as mock_edit:
                    modify_target()
                    mock_edit.assert_called_once_with(fake_short_url, fake_new_target)
                    captured = capsys.readouterr()
                    expected_msg = f"Target successfully updated to: {fake_new_target}"
                    assert expected_msg in captured.out



def test_modify_target_backend_failure(capsys):
    fake_short_url = "short123"
    fake_new_target = "http://nuovo-sito.com"

    with patch('tui.app.same_method', return_value=fake_short_url):
        # 2. Utente inserisce input
        with patch('builtins.input', return_value=fake_new_target):
            # 3. Validazione OK
            with patch('tui.app.validate_url', return_value=fake_new_target):
                # 4. IL CLIENT RESTITUISCE FALSE (Errore Backend)
                with patch('tui.app.client.edit_target', return_value=False) as mock_edit:
                    modify_target()

                    mock_edit.assert_called_once_with(fake_short_url, fake_new_target)

                    captured = capsys.readouterr()
                    assert "Error updating target" in captured.out


def test_modify_target_invalid_input(capsys):
    fake_short_url = "short123"
    fake_invalid_target = "non-è-un-sito"

    with patch('tui.app.same_method', return_value=fake_short_url):
        with patch('builtins.input', return_value=fake_invalid_target):
            with patch('tui.app.validate_url', return_value=None):
                with patch('tui.app.client.edit_target') as mock_edit:
                    modify_target()
                    mock_edit.assert_not_called()
                    captured = capsys.readouterr()
                    assert "Invalid target. Operation canceled." in captured.out


from unittest.mock import patch
from tui.app import modify_target


def test_modify_target_no_selection():
    with patch('tui.app.same_method', return_value=None):
        with patch('builtins.input') as mock_input:
            with patch('tui.app.client.edit_target') as mock_edit:
                modify_target()
                mock_input.assert_not_called()
                mock_edit.assert_not_called()

def test_modify_label_success():
    fake_short_url = "short123"
    fake_label = "Nuova Etichetta"

    with patch('tui.app.same_method', return_value=fake_short_url):
        with patch('builtins.input', return_value=fake_label):
            with patch('tui.app.validate_label', return_value=fake_label):
                with patch('tui.app.client.edit_label') as mock_edit:
                    modify_label()
                    mock_edit.assert_called_once_with(fake_label, fake_short_url)
