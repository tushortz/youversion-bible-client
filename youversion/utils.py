from datetime import datetime

import requests

from youversion import _endpoints as _ep
from youversion.item import Votd


class Client:
    """Client class representing instance to get data from the Youversion API
    """
    def __init__(self, username, password):
        """Initialises the Bible instance so user can retrieve data

        Args:
            username (str): The user's ``username``
            password (str): The user's ``password``
        """

        self.username = username
        self._session = self._get_session(username, password)

    def _get_session(self, username: str, password: str):
        """Get's current user session

        Args:
            username (str): The user's ``username``
            password (str): The user's ``password``

        Returns:
            requests.Session: Returns a session object
        """
        session = requests.Session()
        session.auth = (username, password)

        url = f'{_ep.HOME}{_ep.SIGNIN_URL}'
        session.post(
            url,
            params={
                "username": username,
                "password": password
            })

        return session

    def verse_of_the_day(self, day=None):
        """Returns the verse of the day

        Args:
            day (int, optional): Returns the verse of the dat. Defaults to None.

            If day is None, it returns the verse for the current day

        Returns:
            Votd: A verse of the day object
        """
        response = self._session.get(_ep.VOTD_URL).json()

        if not day:
            day = datetime.now().day

        data = None
        for ref in response.get("votd"):
            if ref["day"] == day:
                data = ref
                return Votd(**data)

        return None

    def _cards(self, options=None):
        """Represents the different kinds of data available

        For example:
            ``votd``,
            ``note``,
            ``highlight``,
            ``bookmark``,
            ``image``,
            ``plan_segment_completion``,
            ``plan_subscription``,
            ``reading_plan_carousel``
        """

        params = {
            "page": 1,
            "kind": ""
        }

        if options:
            params.update(options)

        moment_url = _ep.MOMENTS_URL.format(username=self.username)
        url = f'{_ep.HOME}{moment_url}'

        response = self._session.get(
            url,
            params=params
        )

        return response.json()

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
