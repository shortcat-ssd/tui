import pytest
from unittest.mock import Mock, patch

from tui.menu import Key, Description, Entry, Menu


def test_key_str():
    k = Key("1")
    assert str(k) == "1"


def test_description_str():
    d = Description("MENU 1")
    assert str(d) == "MENU 1"


def test_entry_create_builds_entry():
    called = {"n": 0}

    def on_sel():
        called["n"] += 1

    e = Entry.create("1", "OPZIONE 1", on_sel, is_exit=False)

    assert str(e.key) == "1"
    assert str(e.description) == "OPZIONE 1"
    e.on_selected()
    assert called["n"] == 1
    assert e.is_exit is False


def test_menu_builder_build_requires_exit_entry():
    # Senza entry di exit, build deve fallire
    b = Menu.Builder(Description("MENU"))
    b.with_entry(Entry.create("1", "A", lambda: None, is_exit=False))
    with pytest.raises(Exception):
        b.build()


def test_menu_builder_build_ok_with_exit_entry():
    b = Menu.Builder(Description("MENU"))
    b.with_entry(Entry.create("0", "EXIT", lambda: None, is_exit=True))
    m = b.build()
    assert isinstance(m, Menu)


def test_menu_run_selects_valid_entry_and_exits():
    called = {"auto": 0, "action": 0}

    def auto():
        called["auto"] += 1

    def action():
        called["action"] += 1

    menu = (
        Menu.Builder(Description("MENU"), auto_select=auto)
        .with_entry(Entry.create("1", "DO", action, is_exit=False))
        .with_entry(Entry.create("0", "EXIT", lambda: None, is_exit=True))
        .build()
    )

    # Prima input = "1" (esegue action), poi input = "0" (exit)
    with patch("builtins.input", side_effect=["1", "0"]):
        menu.run()

    assert called["auto"] >= 1
    assert called["action"] == 1


def test_menu_run_invalid_then_valid():
    called = {"action": 0}

    def action():
        called["action"] += 1

    menu = (
        Menu.Builder(Description("MENU"))
        .with_entry(Entry.create("1", "DO", action, is_exit=False))
        .with_entry(Entry.create("0", "EXIT", lambda: None, is_exit=True))
        .build()
    )

    # "X" invalido -> stampa errore e riprova -> poi "1" -> poi "0"
    with patch("builtins.input", side_effect=["X", "1", "0"]), patch("builtins.print") as p:
        menu.run()

    assert called["action"] == 1
    # verifica che abbia stampato il messaggio di errore almeno una volta
    assert any("Invalid selection" in str(args[0]) for args, _ in p.call_args_list)
