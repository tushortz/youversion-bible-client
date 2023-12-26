from datetime import datetime
from typing import List

import requests

from youversion import _endpoints as _ep
from youversion.models import (
    Friendship, Highlight, Image, Note, PlanCompletion, PlanSegmentCompletion,
    PlanSubscription, Reference, Votd,
)
from youversion.models.base import (
    Moment, PlanCompletionAction, PlanSegmentAction,
)
from youversion.models.commons import Action, Comment, Like, User


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

    def _get_references(self, references) -> List[Reference]:
        """Create a list of Reference objects from the given list of dictionaries"""
        references = [
            Reference(
                version_id=ref["version_id"],
                human=ref["human"],
                usfm=ref["usfm"],
            )
            for ref in references
        ]

        return references

    def _cards(self, options=None):
        """Represents the different kinds of data available

        For example:
            ``votd``,
            ``note``,
            ``highlight``,
            ``bookmark``,
            ``image``,
            ``friendship``,
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

    def moments(self, page=1) -> List[Moment]:
        """Get the list of moments available in a specific page

        Arguments:
            page (int): Optional page number. defaults to 1
        """

        mapper = {
            "friendship": Friendship,
            "highlight": Highlight,
            "image": Image,
            "note": Note,
            "plan_completion": PlanCompletion,
            "plan_segment_completion": PlanSegmentCompletion,
            "plan_subscription": PlanSubscription,
        }

        data = self._cards({"page": page})
        moments = []

        for item in data:
            obj: dict = item["object"]
            references = obj.get("references", [])
            kind = item["kind"]
            model = mapper.get(kind)

            comments = obj.get("comments", {})
            comments = Comment(**comments)

            likes = obj.get("likes", {})
            likes = Like(**likes)

            user = obj.get("user", {})
            user = User(**user)

            extra_params = {
                "kind": kind
            }

            actions = obj.get("actions", {})

            if kind == "plan_segment_completion":
                actions = PlanSegmentAction(**actions)
                obj.update({"actions": actions})

            elif kind == "plan_completion":
                actions = PlanCompletionAction(**actions)
                obj.update({"actions": actions})

            elif kind == "friendship":
                pass
            else:
                actions = Action(**actions)
                references = self._get_references(references)

                obj.update({
                    "references": references
                })

            card_item = model(
                **obj,
                **extra_params
            )

            moments.append(card_item)

        return moments

    def highlights(self, page=1):
        """_summary_

        Args:
            page (int, optional): Page number. Defaults to 1.

        Returns:
            _type_: _description_
        """
        cards = self._cards({"kind": "highlight", "page": page})
        items = []

        for item in cards:
            kind = item["kind"]
            card = item["object"]

            actions = card.get("actions", {})
            actions = Action(**actions)

            references = card.get("references", [])
            references = self._get_references(references)

            card["references"] = references
            card["actions"] = actions

            items.append(Highlight(
                kind=kind,
                **card,
            ))

        return items

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

    def plan_progress(self, page=1):
        item = self._cards({"kind": "plan_segment_completion", "page": page})
        return item

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

    # def download_audio(self, version="KJV", ):
    #     pass
