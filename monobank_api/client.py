from datetime import datetime
from .helpers import to_timestamp
from .signature import SignKey
from .transport import api_request
from .errors import Error


class BaseAPI:
    def _get_headers(self, url):
        return {"X-Time": str(to_timestamp(datetime.now()))}

    def make_request(self, method, path, **kwargs):
        headers = self._get_headers(path)
        return api_request(method, path, headers=headers, **kwargs)

    def get_currency(self):
        return self.make_request("GET", "/bank/currency")

    def get_client_info(self):
        return self.make_request("GET", "/personal/client-info")

    def get_statements(self, account, date_from, date_to):
        assert date_from <= date_to
        url = f"/personal/statement/{account}/{to_timestamp(date_from)}/{to_timestamp(date_to)}"
        return self.make_request("GET", url)

    def create_webhook(self, url):
        return self.make_request("POST", "/personal/webhook", json={"webHookUrl": url,})


class PersonalAPI(BaseAPI):
    """
    Personal API
    """

    def __init__(self, token):
        self.token = token

    def _get_headers(self, url):
        return {
            "X-Token": self.token,
        }


class CorporateAPI(BaseAPI):
    """
    Corporate API
    """

    def __init__(self, request_id, private_key):
        self.request_id = request_id
        self.key = SignKey(private_key)

    def _get_headers(self, url):
        headers = {
            "X-Key-Id": self.key.get_key_id(),
            "X-Time": str(to_timestamp(datetime.now())),
            "X-Request-Id": self.request_id,
        }
        data = headers["X-Time"] + headers["X-Request-Id"] + url
        headers["X-Sign"] = self.key.sign(data)
        return headers

    def check(self):
        "Checks if user approved access request"
        try:
            self.make_request("GET", "/personal/auth/request")
            return True
        except Error as e:
            if e.response.status_code == 401:
                return False
            raise


def request_auth(permissions, private_key, callback_url=None):
    """Creates an access request for corporate api user"""
    key = SignKey(private_key)
    headers = {
        "X-Key-Id": key.get_key_id(),
        "X-Time": str(to_timestamp(datetime.now())),
        "X-Permissions": permissions,
    }
    if callback_url:
        headers["X-Callback"] = callback_url
    path = "/personal/auth/request"
    sign_str = headers["X-Time"] + headers["X-Permissions"] + path
    headers["X-Sign"] = key.sign(sign_str)
    return api_request("POST", path, headers=headers)
