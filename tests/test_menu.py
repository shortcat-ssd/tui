from tui.menu import Menu, Entry, Description, Key  # importa dal tuo file

def say_hello():
    print("CIAO dal menu!")

def exit_message():
    print("Uscita dal menu.")


def main():
    # Costruzione menu tramite Builder
    menu = (
        Menu.Builder(Description("Menu di Test"))
            .with_entry(Entry.create("1", "Saluta", say_hello))
            .with_entry(Entry.create("0", "Esci", exit_message, is_exit=True))
            .build()
    )

    # Avvia il menu
    menu.run()


if __name__ == "__main__":
    main()
