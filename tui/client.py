import requests

from tui.domain import Username, Password, Email, ShortUrl, short
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"


class Backend:
    def __init__(self):
        self.session = requests.Session()

    def login(self, username: Username, password: Password):
        response = self.session.post(
            f"{BASE_URL}/auth/login/",
            data={"username": username.value, "password": password.value},
        )
        return response.ok

    def logout(self):
        csrf_token = self.session.cookies.get("csrftoken")
        response = self.session.post(
            f"{BASE_URL}/auth/logout/", headers={"X-CSRFToken": csrf_token}
        )

        if response.ok:
            self.session.cookies.clear()
        else:
            print("Logout failed")

    def register(
        self, username: Username, password1: Password, password2: Password, email: Email
    ):
        response = self.session.post(
            f"{BASE_URL}/auth/registration/",
            data={
                "username": username.value,
                "password1": password1.value,
                "password2": password2.value,
                "email": email.value,
            },
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
                "new_password2": new_pw2,
            },
            headers={"X-CSRFToken": csrf_token},
        )

        if response.ok:
            return True, "Password changed successfully"
        else:
            try:
                return False, response.json()
            except:
                return False, response.text

    def edit_target(self, s: ShortUrl, new_target: str):
        csrf_token = self.session.cookies.get("csrftoken")
        response = self.session.patch(
            f"{BASE_URL}/shorts/{s.code}/",
            json={"target": new_target},
            headers={"X-CSRFToken": csrf_token},
        )
        return response.ok

    def edit_expire(self, s: ShortUrl, new_expire: datetime):

        try:
            csrf_token = self.session.cookies.get("csrftoken")
            response = self.session.patch(
                f"{BASE_URL}/shorts/{s.code}/",
                json={"expired_at": new_expire.isoformat()},
                headers={"X-CSRFToken": csrf_token},
            )

            if response.ok:
                return True, "Expiry updated successfully"
            else:
                return False, f"{response.status_code}: {response.text}"

        except Exception as e:
            return False, str(e)

    def edit_label(self, new_label: str, s: short):
        try:
            csrf_token = self.session.cookies.get("csrftoken")
            response = self.session.patch(
                f"{BASE_URL}/shorts/{s.code}/",
                json={
                    "label": new_label,
                },
                headers={"X-CSRFToken": csrf_token},
            )
            if response.ok:
                return True, "Label changed successfully"
            else:
                return False, f"{response.status_code}: {response.text}"

        except Exception as e:
            return False, str(e)

    def edit_visibility(self, s: ShortUrl, scelta: bool):
        csrf_token = self.session.cookies.get("csrftoken")

        response = self.session.patch(
            f"{BASE_URL}/shorts/{s.code}/",
            json={"private": scelta},
            headers={"X-CSRFToken": csrf_token},
        )

        if response.ok:
            return True, "Visibility changed successfully"
        else:
            return False, response.text

    def edit_username(self, new_username: Username):
        csrf_token = self.session.cookies.get("csrftoken")
        response = self.session.patch(
            f"{BASE_URL}/auth/user/",
            json={"username": new_username},
            headers={"X-CSRFToken": csrf_token},
        )
        if response.ok:
            return True, "Username changed successfully"
        else:
            try:
                return False, response.json()
            except:
                return False, response.text

    def createUrl(self, url: short):
        try:
            csrf_token = self.session.cookies.get("csrftoken")
            response = self.session.post(
                f"{BASE_URL}/shorts/",
                data={
                    "target": url.target,
                    "label": url.label,
                    "expired_at": url.expired_at,
                    "private": url.private,
                },
                headers={"X-CSRFToken": csrf_token},
            )
            if response.ok:
                data = response.json()
                short_code = data.get("code")
                short_url = f"http://localhost:8000/{short_code}"
                return True, short_url
            else:
                return False, f"{response.status_code}: {response.text}"

        except Exception as e:
            return False, str(e)

    def deleteUrl(self, url: ShortUrl):
        try:
            csrf_token = self.session.cookies.get("csrftoken")
            response = self.session.delete(
                f"{BASE_URL}/shorts/{url.code}/", headers={"X-CSRFToken": csrf_token}
            )
            if response.ok:
                return True, "URL deleted successfully."
            else:
                return False, f"{response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)

    def getShortUrl(self):
        try:
            csrf_token = self.session.cookies.get("csrftoken")
            response = self.session.get(
                f"{BASE_URL}/shorts/", headers={"X-CSRFToken": csrf_token}
            )

            if response.ok:
                data = response.json()

                short_urls = [
                    ShortUrl(
                        code=item["code"],
                        target=item["target"],
                        label=item.get("label", ""),
                        private=item.get("private", False),
                        expired_at=item.get("expired_at"),
                        user=None,
                    )
                    for item in data
                ]

                return True, short_urls
            else:
                return False, f"{response.status_code}: {response.text}"

        except Exception as e:
            return False, str(e)