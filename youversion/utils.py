from datetime import datetime

import requests

from youversion import _endpoints as _ep
from youversion.item import Votd, Highlight, Reference, Action


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

    def verse_of_the_day(self, day=None) -> Votd:
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

        for ref in response.get("votd"):
            if ref["day"] == day:
                return Votd(**ref)

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
        data = self._cards({"page": page})
        moments = []

        for item in data:
            obj = item["object"]
            references = obj.get("references", [])

            reference_item = [
                Reference(
                    version_id=ref["version_id"],
                    human=ref["human"],
                    usfm=ref["usfm"],
                )

                for ref in references
            ]

            action_item = obj.get("actions", {})
            action_item = Action(**action_item)

            print(item)
            avatar = obj.get("avatar")
            if avatar and avatar.startswith("//"):
                avatar = "https:" + avatar

            highlight_item = Highlight(
                id=obj["id"],
                kind=item["kind"],
                moment_title=obj["moment_title"],
                created_dt=obj["created_dt"],
                updated_dt=obj["updated_dt"],
                references=reference_item,
                path=obj["path"],
                avatar=avatar,
                time_ago=obj["time_ago"],
                owned_by_me=obj["owned_by_me"],
                actions=action_item
            )

            moments.append(highlight_item)

        return moments

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
