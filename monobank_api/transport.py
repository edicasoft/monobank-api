import requests
from .errors import TooManyRequests, Error

ENDPOINT = "https://api.monobank.ua"
USER_AGENT = "monobank-api (https://github.com/zagran/monobank-api, contact: serhii.z@edicasoft.com)"


def api_request(method, path, **kwargs):
    """
    Handles all HTTP requests for monobank endponts
    """
    headers = kwargs.pop("headers")
    headers["User-Agent"] = USER_AGENT
    url = ENDPOINT + path
    response = requests.request(method, url, headers=headers, **kwargs)

    if response.status_code == 200:
        if not response.content:  # can be just empty an response, but it's fine
            return None
        return response.json()

    if response.status_code == 429:
        raise TooManyRequests("Too many requests", response)

    data = response.json()
    message = data.get("errorDescription", str(data))
    raise Error(message, response)
