import requests

from tui.domain import Username, Password


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
