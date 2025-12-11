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

    def get_csrf_token(self):

        r = self.session.get(f"{BASE_URL}/auth/registration/")
        return self.session.cookies.get("csrftoken")

    def register(self, username: Username, password1: Password, password2: Password, email: Email):
        csrf_token = self.get_csrf_token()
        response = self.session.post(
            f"{BASE_URL}/auth/registration/",
            data={
                "username": username.value,
                "password1": password1.value,
                "password2": password2.value,
                "email": email.value

            },
            headers={"X-CSRFToken": csrf_token}
        )
        if response.ok:
            return True
        else:
            print("Registration failed:", response.status_code, response.text)
            return False
