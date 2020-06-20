import requests
from datetime import datetime


class Bible:
    def __init__(self, username, password, headers=None):
        self.headers = headers or {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "content-type": "application/json; charset=utf-8"
        }

        self.username = username

        self.ENDPOINTS = {
            "home":    "https://my.bible.com",
            "login":   "/sign-in",
            "moments": "/users/{}/_cards.json".format(username),
        }

        self.password = password
        self.session = self.get_session(username, password)

    def get_session(self, username, password):
        session = requests.Session()
        session.auth = (username, password)

        session.post(self.get_url("login"), params={
                     "username": username, "password": password})

        return session

    def get_url(self, url_key):
        return '{}{}'.format(self.ENDPOINTS["home"], self.ENDPOINTS[url_key])

    def votd(self, day=None):
        data = requests.get(
            "https://nodejs.bible.com/api/moments/votd/3.1").json()

        if day == None:
            day = (datetime.today().date() -
                   datetime.today().date().replace(month=1, day=1)).days + 1

        return list(filter(lambda x: x["day"] == day, data.get("votd")))[0]

    def _cards(self, options={}):
        """
            kind -> votd, note, highlight, bookmark, image, plan_segment_completion, plan_subscription
        """

        page = options.get("page", 1)
        kind = options.get("kind", '')

        params = {
            "page": page,
            "kind": kind
        }

        response = self.session.get(self.get_url("moments"), params=params)

        try:
            return response.json()
        except Exception as err:
            return {"error": err}

    def moments(self, page=1):
        return self._cards({"page": page})

    def highlights(self, page=1):
        return self._cards({"kind": "highlight", "page": page})

    def daily_verses(self, page=1):
        return self._cards({"kind": "votd", "page": page})

    def plan_progress(self, page=1):
        return self._cards({"kind": "plan_segment_completion", "page": page})

    def bookmarks(self, page=1):
        return self._cards({"kind": "bookmark", "page": page})

    def my_images(self, page=1):
        return self._cards({"kind": "image", "page": page})

    def notes(self, page=1):
        return self._cards({"kind": "note", "page": page})

    def plan_subscriptions(self, page=1):
        return self._cards({"kind": "plan_subscription", "page": page})

    def convert_note_to_md(self):
        notes = self.notes()
        