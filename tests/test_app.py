from unittest.mock import patch, MagicMock

from tui.app import  same_method


from tui.app import  editmenu
from tui.app import modify_visibility,urls_to_dict, modify_label, submenu, main, build_main_menu
from tui.app import do_login, do_register, logout, edit_password, convert_url, edit_url, delete_url, url_history

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


def test_modify_target_success(capsys):
    fake_short_url = "short123"
    fake_new_target = "http://nuovo-sito.com"

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


@patch('builtins.input', side_effect=['1', 'n'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict', return_value={1: MagicMock(label="label1")})
def test_delete_url_cancelled(mock_urls_to_dict, mock_show, mock_client, mock_print, mock_input):
    mock_client.getShortUrl.return_value = (True, [MagicMock(label="label1")])
    delete_url()
    mock_print.assert_called_with("Deletion cancelled.")

@patch('builtins.input', side_effect=['1', 'y'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict', return_value={1: MagicMock(label="label1")})
def test_delete_url_success(mock_urls_to_dict, mock_show, mock_client, mock_print, mock_input):
    mock_client.getShortUrl.return_value = (True, [MagicMock(label="label1")])
    mock_client.deleteUrl.return_value = (True, "Deleted")
    delete_url()
    mock_print.assert_called_with("Deleted")


@patch('tui.app.client.edit_visibility')
@patch('tui.app.validate_private', return_value=True)
@patch('builtins.input', return_value="yes")
@patch('tui.app.same_method', return_value="short123")
def test_modify_visibility_true_decorator(mock_same, mock_input, mock_val, mock_edit):
    modify_visibility()


    mock_edit.assert_called_once_with("short123", True)

@patch('tui.app.client.edit_visibility')
@patch('tui.app.validate_private', return_value=False)
@patch('builtins.input', return_value="no")
@patch('tui.app.same_method', return_value="short123")
def test_modify_visibility_false_decorator(mock_same, mock_input, mock_val, mock_edit):
    modify_visibility()

    mock_edit.assert_called_once_with("short123", False)




@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict')
@patch('builtins.input')
@patch('tui.app.client.getShortUrl')
def test_same_method_success(mock_get_url, mock_input, mock_urls_to_dict, mock_show):
    fake_item = MagicMock(label="MyLink")
    fake_dict = {1: fake_item}


    mock_get_url.return_value = (True, ["raw_list"])
    mock_urls_to_dict.return_value = fake_dict
    mock_input.return_value = "1"

    result = same_method()


    assert result == fake_item
    mock_show.assert_called_once()


@patch('builtins.print')
@patch('tui.app.client.getShortUrl')
def test_same_method_api_error(mock_get_url, mock_print):
    mock_get_url.return_value = (False, "Network Error")
    result = same_method()
    assert result is None 
    mock_print.assert_called_with("Error fetching URLs:", "Network Error")




@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict')
@patch('builtins.input')
@patch('builtins.print')
@patch('tui.app.client.getShortUrl')
def test_same_method_invalid_digit(mock_get_url, mock_print, mock_input, mock_to_dict, mock_show):
    mock_get_url.return_value = (True, [])
    mock_to_dict.return_value = {}
    mock_input.return_value = "abc"


    result = same_method()


    assert result is None
    mock_print.assert_called_with("Invalid input. Please enter a number.")

@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict')
@patch('builtins.input')
@patch('builtins.print')
@patch('tui.app.client.getShortUrl')
def test_same_method_out_of_range(mock_get_url, mock_print, mock_input, mock_to_dict, mock_show):

    fake_dict = {1: "item1", 2: "item2"}
    mock_get_url.return_value = (True, [])
    mock_to_dict.return_value = fake_dict
    mock_input.return_value = "5"


    result = same_method()

    assert result is None
    mock_print.assert_called_with("Invalid choice. Number out of range.")

@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict')
@patch('tui.app.client')
def test_url_history_success(mock_client, mock_urls_to_dict, mock_show):

    mock_url_item = MagicMock(label="label1", target="http://example.com")
    mock_client.getShortUrl.return_value = (True, [mock_url_item])

    mock_urls_to_dict.return_value = {1: mock_url_item}

    url_history()

    mock_urls_to_dict.assert_called_once_with([mock_url_item])

    mock_show.assert_called_once_with({1: mock_url_item})


@patch('builtins.input', side_effect=['1', 'y'])
@patch('builtins.print')
@patch('tui.app.client')
@patch('tui.app.show_urls_dict')
@patch('tui.app.urls_to_dict')
def test_delete_url_failure(mock_urls_to_dict, mock_show, mock_client, mock_print, mock_input):
    mock_url_item = MagicMock(label="label1", target="http://example.com")
    mock_client.getShortUrl.return_value = (True, [mock_url_item])

    mock_urls_to_dict.return_value = {1: mock_url_item}

    mock_client.deleteUrl.return_value = (False, "Some error")

    delete_url()

    mock_print.assert_any_call("Error:", "Some error")


@patch('tui.app.Menu.Builder')
def test_editmenu_runs_menu(mock_builder_class):

    mock_builder_instance = MagicMock()
    mock_builder_class.return_value = mock_builder_instance


    mock_builder_instance.with_entry.return_value = mock_builder_instance
    menu_mock = MagicMock(name="menu_instance")
    mock_builder_instance.build.return_value = menu_mock

    with patch('builtins.print') as mock_print:
        editmenu()


    mock_print.assert_called_with("\n============= EDIT MENU ==============")


    menu_mock.run.assert_called_once()
def test_urls_to_dict_populated():
    obj1 = MagicMock(label="Link1")
    obj2 = MagicMock(label="Link2")

    input_list = [obj1, obj2]


    result = urls_to_dict(input_list)

    assert len(result) == 2
    assert result[1] == obj1
    assert result[2] == obj2


def test_urls_to_dict_empty():
    input_list = []
    result = urls_to_dict(input_list)

    assert result == {}
    assert len(result) == 0


from unittest.mock import MagicMock
from tui.app import show_urls_dict



def test_show_urls_dict_empty(capsys):

    show_urls_dict({})


    captured = capsys.readouterr()
    assert "No URLs found." in captured.out



def test_show_urls_dict_long_and_date(capsys):

    long_target = "h" * 60
    long_label = "L" * 30

    mock_url = MagicMock()
    mock_url.code = "ABC12"
    mock_url.target = long_target
    mock_url.label = long_label
    mock_url.private = False
    mock_url.expired_at = "2025-12-25T15:30:00Z"  # Formato ISO

    urls_dict = {1: mock_url}

    show_urls_dict(urls_dict)

    captured = capsys.readouterr()

    expected_target_display = ("h" * 47) + "..."
    assert expected_target_display in captured.out

    expected_label_display = ("L" * 17) + "..."
    assert expected_label_display in captured.out

    assert "25/12/2025 15:30" in captured.out



def test_show_urls_dict_short_no_date(capsys):
    # SETUP
    mock_url = MagicMock()
    mock_url.code = "XYZ99"
    mock_url.target = "http://short.com"
    mock_url.label = "MyLabel"
    mock_url.private = True
    mock_url.expired_at = None
    urls_dict = {1: mock_url}

    show_urls_dict(urls_dict)


    captured = capsys.readouterr()


    assert "http://short.com" in captured.out


    assert "MyLabel" in captured.out

    assert "N/A" in captured.out


from unittest.mock import patch
from tui.app import edit_username


# --- CASO POSITIVO (SUCCESS) ---
# Copre il ramo IF: API risponde True -> Stampa successo

@patch('tui.app.client.edit_username')  # Mock API
@patch('tui.app.Username')  # Mock della classe di dominio
@patch('builtins.input')  # Mock input utente
def test_edit_username_success(mock_input, mock_username_cls, mock_edit, capsys):
    # SETUP
    # 1. input viene chiamato DUE volte:
    #    - Prima volta: Inserisce il nuovo username "NewName"
    #    - Seconda volta: Preme Invio alla fine ("")
    mock_input.side_effect = ["NewName", ""]

    # 2. Quando viene chiamato Username("NewName"), facciamo restituire la stringa stessa
    #    Così quando viene stampata nell'f-string, leggiamo "NewName" e non <MagicMock...>
    mock_username_cls.side_effect = lambda x: x

    # 3. L'API risponde con successo
    mock_edit.return_value = (True, "Success message")

    # ESECUZIONE
    edit_username()

    # VERIFICHE
    # Verifica che il client sia stato chiamato con "NewName"
    mock_edit.assert_called_once_with("NewName")

    # Verifica il messaggio di stampa
    captured = capsys.readouterr()
    assert "Username Updated: NewName!" in captured.out



@patch('tui.app.client.edit_username')
@patch('tui.app.Username')
@patch('builtins.input')
def test_edit_username_failure(mock_input, mock_username_cls, mock_edit, capsys):

    mock_input.side_effect = ["BadName", ""]  # Username inserito e poi Invio
    mock_username_cls.side_effect = lambda x: x  # Username("BadName") -> "BadName"

    mock_edit.return_value = (False, "Username already taken")

    edit_username()

    mock_edit.assert_called_once_with("BadName")

    captured = capsys.readouterr()
    assert "Error: Username already taken" in captured.out


from unittest.mock import patch
from tui.app import edit_password


# --- CASO POSITIVO (SUCCESS) ---
# Copre il flusso: getpass x3 -> Password x3 -> API OK -> Print Success -> Input

@patch('tui.app.client.edit_password')  # Mock chiamata API
@patch('tui.app.Password')  # Mock classe di dominio
@patch('tui.app.getpass')  # Mock input nascosto
@patch('builtins.input')  # Mock input finale (pausa)
def test_edit_password_success(mock_input, mock_getpass, mock_pw_cls, mock_edit, capsys):
    # SETUP
    # 1. getpass viene chiamato 3 volte. Definiamo la sequenza di risposte:
    mock_getpass.side_effect = ["OldPass", "NewPass", "NewPass"]

    # 2. Quando il codice fa Password("OldPass"), facciamo restituire la stringa "OldPass"
    #    Così è più facile verificare con cosa è stato chiamato il client.
    mock_pw_cls.side_effect = lambda x: x

    # 3. Il client risponde con successo (True)
    mock_edit.return_value = (True, "Success msg")

    # ESECUZIONE
    edit_password()

    # VERIFICHE
    # Verifica che il client sia stato chiamato con le 3 password corrette
    mock_edit.assert_called_once_with("OldPass", "NewPass", "NewPass")

    # Verifica il messaggio di successo stampato
    captured = capsys.readouterr()
    assert "Password updated" in captured.out

    # Verifica che sia stato chiamato l'input finale per la pausa
    mock_input.assert_called_once()



@patch('tui.app.client.edit_password')
@patch('tui.app.Password')
@patch('tui.app.getpass')
@patch('builtins.input')
def test_edit_password_failure(mock_input, mock_getpass, mock_pw_cls, mock_edit, capsys):
    mock_getpass.side_effect = ["OldPass", "NewPass", "WrongConfirm"]

    mock_pw_cls.side_effect = lambda x: x

    mock_edit.return_value = (False, "Passwords do not match")

    edit_password()

    mock_edit.assert_called_once_with("OldPass", "NewPass", "WrongConfirm")

    captured = capsys.readouterr()
    assert "Error: Passwords do not match" in captured.out


@patch('tui.app.Menu.Builder')
def test_submenu_runs_menu(mock_builder_class):
    mock_builder_instance = MagicMock()
    mock_builder_class.return_value = mock_builder_instance


    mock_builder_instance.with_entry.return_value = mock_builder_instance
    menu_mock = MagicMock(name="menu_instance")
    mock_builder_instance.build.return_value = menu_mock

    # Patch di print
    with patch('builtins.print') as mock_print:
        submenu()

    mock_print.assert_called_with("\n============= USER MENU  ==============")


    menu_mock.run.assert_called_once()



@patch('tui.app.Menu.Builder')
@patch('tui.app.Description')
def test_build_main_menu(mock_description, mock_builder_class):
    mock_builder_instance = MagicMock()
    mock_builder_class.return_value = mock_builder_instance
    mock_builder_instance.with_entry.return_value = mock_builder_instance

    menu_mock = MagicMock(name="menu_instance")
    mock_builder_instance.build.return_value = menu_mock

    # Chiama direttamente la funzione di costruzione
    build_main_menu()

    mock_builder_class.assert_called_once_with(mock_description.return_value)
    mock_builder_instance.build.assert_called_once()
    menu_mock.run.assert_called_once()