from getpass import getpass

from pyexpat.errors import messages
from valid8 import ValidationError

from .client import Backend
from .domain import Username, Password, Email, ShortUrl, short
from .menu import Menu, Entry, Description, Key
from datetime import datetime


client = Backend()



def do_login():
    print("\n--- LOGIN ---")
    while True:
        try:
            raw_user = input("Username: ").strip()
            user = Username(raw_user)
            print(f"DEBUG: username ok: {user}")

            raw_pass = getpass("Password: ").strip()
            pw = Password(raw_pass)

            if client.login(user, pw):
                print("\nLogin successful.")
                submenu()
                break
            else:
                print("\nWrong username or password.")

        except ValidationError as e:
            raise ValidationError(e)
            print(f"Error: {e}. Try again.\n")


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

            confirm_password = getpass("Confirm password: ").strip()
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
            print(f"Error: {e}. Try Again.\n")


def logout():
    client.logout()
    print("Logged out.\n")




def convert_url():
    print("\n--- URL CONVERSATION ---")

    raw_url = input("URL: ").strip()
    raw_label = input("Label: ").strip()
    expiry_str = input("Expiry Date and Time (YYYY-MM-DD HH:MM, optional): ").strip()

    private_input = input("Private (yes/no): ").strip().lower()

    if private_input in ["yes", "y", "true", "1"]:
        private = True
    else:
        private = False

    print(private)

    if not raw_url:
        print("Invalid Url, Try again.\n")
        return

    expiry_datetime = None
    if expiry_str:
        try:
            expiry_datetime = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD HH:MM\n")
            return

    s = short(raw_url, raw_label, expiry_datetime, private)
    ok, short_url_or_error = client.createUrl(s)


    if ok:
        print(f"Short Url Created in app.py: {short_url_or_error}\n")
    else:
        print(f"Conversion Error: {short_url_or_error}\n")


def edit_url():
   editmenu()


def delete_url():
    ok, lista = client.getShortUrl()
    if not ok:
        print("Errore nel recupero degli URL:", lista)
        return

    dict_urls = urls_to_dict(lista)
    show_urls_dict(dict_urls)

    scelta = input("Quale URL desideri eliminare? (numero) ").strip()
    if not scelta.isdigit():
        print("Inserisci un numero valido.")
        return
    scelta = int(scelta)

    if scelta not in dict_urls:
        print("Numero non valido.")
        return

    item = dict_urls[scelta]

    conferma = input(f"Sei sicuro di voler eliminare l'URL '{item.label}'? (y/n): ").strip().lower()
    if conferma not in ["y", "yes"]:
        print("Eliminazione annullata.")
        return

    ok, text = client.deleteUrl(item)
    if ok:
        print(text)
    else:
        print("Errore:", text)





def url_history():
    ok, lista = client.getShortUrl()
    dict = urls_to_dict(lista)
    show_urls_dict(dict)



def modify_expire():
    short_url = same_method()
    if not short_url:
        return

    expiry_input = input("Inserisci la nuova data di scadenza (YYYY-MM-DD HH:MM) o 0 per annullare: ").strip()
    if expiry_input == "0":
        return

    try:
        expiry_datetime = datetime.strptime(expiry_input, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Formato data non valido. Usa YYYY-MM-DD HH:MM")
        return

    ok, msg = client.edit_expire(short_url, expiry_datetime)
    if ok:
        print("Data di scadenza aggiornata!")
    else:
        print(f"Errore: {msg}")


def modify_target():
    short_url = same_method()

    #TODO: validazioni sull'input
    if not short_url:
        return

    nuova_target = input("Inserisci il nuovo target: ").strip()
    if not nuova_target:
        print("Target non valido. Operazione annullata.")
        return

    ok = client.edit_target(short_url, nuova_target)
    if ok:
        print(f"Target aggiornato con successo a: {nuova_target}")
    else:
        print("Errore durante l'aggiornamento del target.")


def modify_label():
    short_url = same_method()
    if not short_url:
        return None

    scelta = input("Inserisci la nuova label: ").strip()
    #TODO: VALIDAZIONIIIII
    client.edit_label(scelta, short_url)



def modify_visibility():
    short_url = same_method()
    scelta = input("Inserisci la nuova visibilità: ").strip()
    if scelta in ["yes", "y", "true", "1"]:
        scelta = True
    else:
        scelta= False

    client.edit_visibility(short_url, scelta)


def same_method():
    ok, lista = client.getShortUrl()
    if not ok:
        print("Errore nel recupero degli short URL:", lista)
        return None

    dict = urls_to_dict(lista)
    show_urls_dict(dict)

    scelta = input("Indicare il numero dell'url da modificare: ").strip()
    scelta = int(scelta)

    item = dict[scelta]
    print("SHORT SELEZIONATO: ", item)
    return item




def urls_to_dict(lista):
    urls_dict = {}
    i = 0

    for item in lista:
       i+=1
       urls_dict[i] = item

    return urls_dict


def show_urls_dict(urls_dict):
    if not urls_dict:
        print("Nessun URL trovato.\n")
        return


    header = f"{'N°':<4} | {'CODE':<10} | {'TARGET':<50} | {'LABEL':<20} | {'PRIVATE':<7} | {'EXPIRE':<20}"
    print("*" * len(header))
    print(header)
    print("*" * len(header))


    for key, s in urls_dict.items():
        target = (s.target[:47] + '...') if len(s.target) > 50 else s.target  # tronca se troppo lungo
        label = (s.label[:17] + '...') if len(s.label) > 20 else s.label
        expire = s.expired_at if s.expired_at else "N/A"
        print(f"{key:<4} | {s.code:<10} | {target:<50} | {label:<20} | {str(s.private):<7} | {expire:<20}")

    print("*" * len(header))
    print()






def edit_username():
    new_username = input("New Username: ").strip()
    ok, text = client.edit_username(new_username)
    if ok:
        print(f"\nUsername Updated: {new_username}! Click send to go back to the menu.")
    else:
        print(f"\nError: {text}. Click send to go back to the menu.")
    input("")


def edit_password():
    old_pw = getpass("Old password: ").strip()
    new_pw1 = getpass("New password: ").strip()
    new_pw2 = getpass("Confirm new password: ").strip()

    ok, text = client.edit_password(old_pw, new_pw1, new_pw2)
    if ok:
        print("\n Password updated. Click send to go back to the menu.")
    else:
        print(f"\nError: {text}. Click send to go back to the menu")
    input("")


def editmenu():
    print("\n============= EDIT MENU ==============")
    menu = (
        Menu.Builder(Description("EDIT URL"))
        .with_entry(Entry.create("1", "TARGET", modify_target))
        .with_entry(Entry.create("2", "LABEL", modify_label))
        .with_entry(Entry.create("3", "PRIVATE", modify_visibility))
        .with_entry(Entry.create("4", "EXPIRE AT", modify_expire))
        .with_entry(Entry.create("0", "BACK", lambda: True, is_exit=True))
        .build()
    )
    menu.run()


def submenu():
    print("\n============= USER MENU  ==============")
    menu = (
        Menu.Builder(Description("USER OPTIONS"))
        .with_entry(Entry.create("1", "CONVERT URL", convert_url))
        .with_entry(Entry.create("2", "EDIT SHORT", edit_url))
        .with_entry(Entry.create("3", "DELETE URL", delete_url))
        .with_entry(Entry.create("4", "CHRONOLOGY URL", url_history))
        .with_entry(Entry.create("6", "EDIT USERNAME", edit_username))
        .with_entry(Entry.create("7", "EDIT PASSWORD", edit_password))
        .with_entry(Entry.create("0", "BACK", lambda: True, is_exit=True))
        .build()
    )
    menu.run()



def main():
    menu = (
        Menu.Builder(Description("MENU"))
        .with_entry(Entry.create("1", "Login", do_login))
        .with_entry(Entry.create("2", "Registration", do_register))
        .with_entry(Entry.create("0", "Exit", logout, is_exit=True))
        .build()
    )
    menu.run()



if __name__ == "__main__":
    main()
