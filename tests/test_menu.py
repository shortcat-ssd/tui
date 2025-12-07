from tui.menu import Menu, Entry, Description, Key

def say_hello():
    print("Benvenuto!")

def exit_message():
    print("Uscita dal menu.")


def main():
    menu = (
        Menu.Builder(Description("Menu di Test"))
            .with_entry(Entry.create("1", "Entra", say_hello))
            .with_entry(Entry.create("0", "Esci", exit_message, is_exit=True))
            .build()
    )

    # Avvia il menu
    menu.run()


if __name__ == "__main__":
    main()
