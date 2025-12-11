from getpass import getpass

from valid8 import ValidationError

from tui.client import Backend
from tui.domain import Username, Password, Email
from tui.menu import Menu, Entry, Description, Key




client = Backend()

def do_login():
    print("\n--- LOGIN ---")

    while True:
        try:
            raw_user = input("Username: ").strip()
            user = Username(raw_user)

            raw_pass = getpass("Password: ").strip()
            pw = Password(raw_pass)


            if client.login(user, pw):
                print("\nLogin successfull.")
                submenu()
                break
            else:
                print("\nWrong username or password.")


        except ValidationError as e:
            print(f"Error: {e}. Riprova.\n")


def logout():
    client.logout()

#TODO: sistemare l'invio dell'email per la registrazione -> fallisce

def do_register():
    print("\n--- REGISTRATION ---")
    while True:
        try:
            raw_user = input("Username: ").strip()
            user = Username(raw_user)

            raw_email = input("Email: ").strip()
            email = Email(raw_email)

            password = getpass("Password: ").strip()
            pw1 = Password(password)

            confirm_password = getpass("Confirmation password: ").strip()
            pw2 = Password(confirm_password)


            if pw1.value != pw2.value:
                print("Passwords do not match. Try again.\n")
                continue

            if client.register(user, pw1, pw2, email):
                print("\nRegistration successful. You can now log in.")
                if client.login(user, pw1):
                    print("\nLogin successful.")
                    submenu()
                    break
            else:
                print("\nRegistration failed. Try again.")

        except ValidationError as e:
            print(f"Error: {e}. Riprova.\n")




def convert_url():
    print("Funzione convert_url ancora da implementare.")

def edit_url():
    print("Funzione edit_url ancora da implementare.")

def delete_url():
    print("Funzione delete_url ancora da implementare.")

def url_history():
    print("Funzione url_history ancora da implementare.")

def url_info():
    print("Funzione url_info ancora da implementare.")

def edit_username():
    print("Funzione da implementare.")





def edit_password():
    old_pw = getpass("Vecchia password: ").strip()
    new_pw1 = getpass("Nuova password: ").strip()
    new_pw2 = getpass("Conferma nuova password: ").strip()

    ok, text = client.edit_password(old_pw, new_pw1, new_pw2)
    if ok:
        print("\nPassword aggiornata! Premi invio per tornare al menu.")
    else:
        print(f"\nErrore: {text}. Premi invio per tornare al menu.")

    input("")  # Pausa prima che il menu si riavvii

def submenu():


    print("\n============= MENU ==============")

    menu = (
        Menu.Builder(Description(" OPZIONI "))
        .with_entry(Entry.create("1", "Converti url", convert_url))
        .with_entry(Entry.create("2", "Modifica url", edit_url))
        .with_entry(Entry.create("3", "Elimina url", delete_url))
        .with_entry(Entry.create("4", "Cronologia url", url_history))
        .with_entry(Entry.create("5", "Informazioni specifiche di un url", url_info))
        .with_entry(Entry.create("6", "Modifica username", edit_username))
        .with_entry(Entry.create("7", "Modifica password", edit_password))
        .with_entry(Entry.create("0", "Logout", logout, is_exit=True))
        .build()
    )

    menu.run()



def main():
    menu = (
        Menu.Builder(Description("Menu di Test"))
            .with_entry(Entry.create("1", "Login",do_login))
            .with_entry(Entry.create("2", "Register", do_register))
            .with_entry(Entry.create("0", "Logout", logout, is_exit=True))
            .build()
    )

    # Avvia il menu
    menu.run()


if __name__ == "__main__":
    main()
