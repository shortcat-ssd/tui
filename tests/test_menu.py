from getpass import getpass
from gettext import gettext

from valid8 import ValidationError

from tui.domain import Username, Password
from tui.menu import Menu, Entry, Description, Key

def do_login():
    print("\n--- LOGIN ---")

    while True:
        try:
            raw_user = input("Username: ").strip()
            user = Username(raw_user)

            raw_pass = getpass("Password: ").strip()
            pw = Password(raw_pass)

            print("\nLogin successfull.")
            break

        except ValidationError as e:
            print(f"Error: {e}. Riprova.\n")


def exit_message():
    print("Uscita dal menu.")


def main():
    menu = (
        Menu.Builder(Description("Menu di Test"))
            .with_entry(Entry.create("1", "Entra",do_login))
            .with_entry(Entry.create("0", "Esci", exit_message, is_exit=True))
            .build()
    )

    # Avvia il menu
    menu.run()


if __name__ == "__main__":
    main()
