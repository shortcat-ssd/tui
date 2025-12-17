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
    print("\Logged out.\n")




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


#=================== DA IMPLEMENTARE ====================

def delete_url():
    print("Funzione delete_url ancora da implementare.")

def url_info():
    print("Funzione url_info ancora da implementare.")


def modify_target():
    pass



def modify_expire():
    pass








def url_history():
    ok, lista = client.getShortUrl()
    dict = urls_to_dict(lista)
    show_urls_dict(dict)




def show_urls(lista):
    if not lista:
        print("Nessun URL trovato.\n")
        return

    only_lista = lista[1]
    #print(only_lista)

    for url in only_lista:
        #print("Oggetto", url, end="\n")
        code = url["code"]
        visibility = url["visibility"]
        expire = url["expire"]
        target = url["target"]
        label = url["label"]

        print("CODE", code,"VISIBILITY", visibility, "EXPIRE", expire,"TARGET", target, "LABEL", label, end="\n")






def modify_label():
    short_url = same_method()
    scelta = input("Inserisci la nuova label: ").strip()
    #TODO: VALIDAZIONIIIII
    print("Stampa in modify label", short_url)
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

    for key, s in urls_dict.items():
        print(
            f"{key}) CODE: {s.code}, TARGET: {s.target}, LABEL: {s.label}, "
            f"PRIVATE: {s.private}, EXPIRE: {s.expired_at}"
        )



def show_urls_(urls_dict):
    """
    Stampa in modo leggibile un dizionario di URL.
    """
    if not urls_dict:
        print("Nessun URL trovato.\n")
        return

    for key, url_data in urls_dict.items():
        # Se url_data è un dizionario con più proprietà
        if isinstance(url_data, dict):
            print(
                f"{key},"
                f"CODE: {url_data.get('code')}, "
                f"TARGET: {url_data.get('target')}, "
                f"LABEL: {url_data.get('label')}, "
                f"VISIBILITY: {url_data.get('visibility')}, "
                f"EXPIRE: {url_data.get('expire')}"
            )
        else:
            # Se url_data è semplicemente il target
            print(f"KEY: {key}, VALUE: {url_data}")




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
        print("\n password updated. Click send to go back to the menu.")
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
        .with_entry(Entry.create("0", "LOG OUT", logout, is_exit=True))
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
        .with_entry(Entry.create("5", "INFO URL", url_info))
        .with_entry(Entry.create("6", "EDIT USERNAME", edit_username))
        .with_entry(Entry.create("7", "EDIT PAASWORD", edit_password))
        #.with_entry(Entry.create("0", "BACK", back_to_submenu))
        .with_entry(Entry.create("0", "LOGOUT", logout, is_exit=True))
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
