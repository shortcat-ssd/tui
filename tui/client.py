import requests

from tui.domain import Username, Password, Email

BASE_URL = "http://localhost:8000/api/v1"

class Backend:
    def __init__(self):
        self.session = requests.Session()


    def login(self, username: Username, password: Password):
        response = self.session.post(
            f"{BASE_URL}/auth/login/",
            data={
                "username": username.value,
                "password": password.value
            }
        )
        return response.ok


    def logout(self):
        csrf_token = self.session.cookies.get("csrftoken")
        response = self.session.post(
            f"{BASE_URL}/auth/logout/",
            headers={"X-CSRFToken": csrf_token}
        )

        if response.ok:
            self.session.cookies.clear()
            print("Logged out")
        else:
            print("Logout failed")



    def register(self, username: Username, password1: Password, password2: Password, email: Email):
        response = self.session.post(
            f"{BASE_URL}/auth/registration/",
            data={
                "username": username.value,
                "password1": password1.value,
                "password2": password2.value,
                "email": email.value

            }
        )
        if response.ok:
            return True
        else:
            print("Registration failed:", response.status_code, response.text)
            return False


    def edit_password(self, old_pw, new_pw1, new_pw2):
        if new_pw1 != new_pw2:
            return False, "New passwords do not match"

        csrf_token = self.session.cookies.get("csrftoken")
        response = self.session.post(
            f"{BASE_URL}/auth/password/change/",
            json={
                "old_password": old_pw,
                "new_password1": new_pw1,
                "new_password2": new_pw2
            },
            headers={"X-CSRFToken": csrf_token}
        )

        if response.ok:
            return True, "Password changed successfully"
        else:
            try:
                return False, response.json()
            except:
                return False, response.text
