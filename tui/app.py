from getpass import getpass

from django.core.exceptions import ValidationError

from tui.validators import (
    validate_label,
    validate_expired_at,
    validate_private,
    validate_url,
)
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

            raw_pass = getpass("Password: ").strip()
            pw = Password(raw_pass)

            if client.login(user, pw):
                print("\nLogin successful.")
                submenu()
                break
            else:
                print("\nWrong username or password.")

        except ValueError as e:
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


    private = private_input in ["yes", "y", "true", "1"]

    try:

        raw_url = validate_url(raw_url)
        raw_label = validate_label(raw_label)
        private = validate_private(private)

        expiry_datetime = None
        if expiry_str:
            try:
                expiry_datetime = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD HH:MM\n")
                return
            expiry_datetime = validate_expired_at(expiry_datetime)

    except ValidationError as e:
        print(f"Error in input: {e}")
        return


    s = short(raw_url, raw_label, expiry_datetime, private)
    ok, short_url_or_error = client.createUrl(s)

    if ok:
        print(f"Short URL created: {short_url_or_error}\n")
    else:
        print(f"Conversion Error: {short_url_or_error}\n")


def edit_url():
    editmenu()


def delete_url():
    ok, lista = client.getShortUrl()
    if not ok:
        print("Error fetching URLs:", lista)
        return

    dict_urls = urls_to_dict(lista)
    show_urls_dict(dict_urls)

    scelta = input("Which URL do you want to delete? (number) ").strip()
    if not scelta.isdigit():
        print("Enter valid number.")
        return
    scelta = int(scelta)

    if scelta not in dict_urls:
        print("Invalid number.")
        return

    item = dict_urls[scelta]

    conferma = (
        input(f"Are you sure you want to delete the URL? '{item.label}'? (y/n): ")
        .strip()
        .lower()
    )
    if conferma not in ["y", "yes"]:
        print("Deletion cancelled.")
        return

    ok, text = client.deleteUrl(item)
    if ok:
        print(text)
    else:
        print("Error:", text)


def url_history():
    ok, lista = client.getShortUrl()
    dict = urls_to_dict(lista)
    show_urls_dict(dict)


def modify_expire():
    short_url = same_method()
    if not short_url:
        return

    expiry_input = input(
        "Enter the new expiration date (YYYY-MM-DD HH:MM) or 0 to cancel: "
    ).strip()
    if expiry_input == "0":
        return

    try:
        expiry_datetime = datetime.strptime(expiry_input, "%Y-%m-%d %H:%M")
        expiry_datetime = validate_expired_at(expiry_datetime)
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD HH:MM")
        return

    ok, msg = client.edit_expire(short_url, expiry_datetime)
    if ok:
        print("Updated expiration date!")
    else:
        print(f"Error: {msg}")


def modify_target():
    short_url = same_method()

    if not short_url:
        return

    nuovo_target = input("Enter the new target: ").strip()
    nuovo_target = validate_url(nuovo_target)
    if not nuovo_target:
        print("Invalid target. Operation canceled.")
        return

    ok = client.edit_target(short_url, nuovo_target)
    if ok:
        print(f"Target successfully updated to: {nuovo_target}")
    else:
        print("Error updating target")


def modify_label():
    short_url = same_method()
    if not short_url:
        return None

    label = input("Enter the new label: ").strip()
    label = validate_label(label)

    client.edit_label(label, short_url)


def modify_visibility():
    short_url = same_method()
    scelta = input("Enter the new visibility: ").strip()
    if scelta in ["yes", "y", "true", "1"]:
        scelta = True
    else:
        scelta = False

    scelta = validate_private(scelta)
    client.edit_visibility(short_url, scelta)


def same_method():
    ok, lista = client.getShortUrl()
    if not ok:
        print("Error fetching URLs:", lista)
        return None

    dict = urls_to_dict(lista)
    show_urls_dict(dict)

    scelta = input("Enter the URL number to edit: ").strip()
    if not scelta.isdigit():
        print("Invalid input. Please enter a number.")
        return None

    scelta = int(scelta)

    if scelta not in dict:
        print("Invalid choice. Number out of range.")
        return None

    item = dict[scelta]
    return item


def urls_to_dict(lista):
    urls_dict = {}
    i = 0

    for item in lista:
        i += 1
        urls_dict[i] = item

    return urls_dict


def show_urls_dict(urls_dict):
    if not urls_dict:
        print("No URLs found.\n")
        return

    header = f"{'N°':<4} | {'CODE':<10} | {'TARGET':<50} | {'LABEL':<20} | {'PRIVATE':<7} | {'EXPIRE':<20}"
    print("*" * len(header))
    print(header)
    print("*" * len(header))

    for key, s in urls_dict.items():
        target = (
            (s.target[:47] + "...") if len(s.target) > 50 else s.target
        )  # tronca se troppo lungo
        label = (s.label[:17] + "...") if len(s.label) > 20 else s.label

        if s.expired_at:
            dt = datetime.fromisoformat(s.expired_at.replace("Z", ""))
            expire = dt.strftime("%d/%m/%Y %H:%M")
        else:
            expire = "N/A"
        print(
            f"{key:<4} | {s.code:<10} | {target:<50} | {label:<20} | {str(s.private):<7} | {expire:<20}"
        )

    print("*" * len(header))
    print()


def edit_username():
    new_username = input("New Username: ").strip()
    new_username = Username(new_username)
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

    old_pw = Password(old_pw)
    new_pw1 = Password(new_pw1)
    new_pw2 = Password(new_pw2)

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


def main(name: str):
    if __name__ == "__main__":
        menu = (
            Menu.Builder(Description("MENU"))
            .with_entry(Entry.create("1", "Login", do_login))
            .with_entry(Entry.create("2", "Registration", do_register))
            .with_entry(Entry.create("0", "Exit", logout, is_exit=True))
            .build()
        )
        menu.run()


main(__name__)
