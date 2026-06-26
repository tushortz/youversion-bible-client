Data Models
===========

The client uses three complementary model layers:

1. **Dynamic Pydantic models** — generated at runtime from API responses (moments, highlights, plans, etc.)
2. **Protocol type aliases** — static typing hints for common response shapes
3. **Static Pydantic models** — request payloads for creating moments

See :doc:`dynamic_models` for how runtime model generation works.

Dynamic Response Models
-----------------------

Most client methods return dynamically created Pydantic instances or plain ``dict``/``list`` wrappers. There is no fixed ``Highlight``, ``Note``, or ``Image`` class to import — the API response shape drives the model.

.. code-block:: python

   from youversion import SyncClient

   with SyncClient() as client:
       # Each item is a runtime-generated Pydantic model
       for highlight in client.highlights():
           print(highlight.id, highlight.moment_title)

       for note in client.notes():
           print(note.content)

       progress = client.plan_progress()
       subscriptions = client.plan_subscriptions()

Moment kinds are distinguished by ``kind_id`` (or ``kind``) on the returned object, not by separate Python classes.

Static Request Models
---------------------

Use these when **creating** moments via ``create_moment``:

CreateMoment
~~~~~~~~~~~~

.. autoclass:: youversion.models.moments.CreateMoment
   :members:
   :no-index:

ReferenceCreate
~~~~~~~~~~~~~~~

.. autoclass:: youversion.models.moments.ReferenceCreate
   :members:
   :no-index:

.. code-block:: python

   from youversion.enums import MomentKinds, StatusEnum
   from youversion.models.moments import CreateMoment, ReferenceCreate
   from youversion import SyncClient

   payload = CreateMoment(
       kind=MomentKinds.NOTE,
       title="Study note",
       content="Key takeaway from today's reading",
       body="",
       color="ffff00",
       status=StatusEnum.PRIVATE,
       labels=["study"],
       language_tag="en",
       references=[
           ReferenceCreate(
               human="John 3:16",
               version_id=111,
               usfm=["JHN.3.16"],
           )
       ],
   )

   with SyncClient() as client:
       client.create_moment(payload)

Protocol Type Aliases
---------------------

Protocols describe expected fields on dynamic models. Import them for type hints and IDE support; they are **not** constructors.

Base protocols (``youversion.models.base``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: youversion.models.base.MomentProtocol
   :members:
   :no-index:

.. autoclass:: youversion.models.base.ReferenceProtocol
   :members:
   :no-index:

``Moment`` and ``Reference`` are type aliases for these protocols.

.. code-block:: python

   from youversion.models.base import Moment, Reference

   def title_for(moment: Moment) -> str:
       base = moment.base or {}
       title = base.get("title") or {}
       return str(title.get("l_str", ""))

Commons protocols (``youversion.models.commons``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shared nested structures on moment objects:

* ``User`` / ``UserProtocol`` — user embedded in moments
* ``Action`` / ``ActionProtocol`` — deletable, editable, read, show flags
* ``Comment`` / ``CommentProtocol`` — commenting metadata
* ``Like`` / ``LikeProtocol`` — liking metadata
* ``BodyImage`` / ``BodyImageProtocol`` — image dimensions and URL
* ``ReactionModel`` / ``ReactionModelProtocol`` — base for comment/like shapes

Bible protocols (``youversion.models.bible``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``Language``, ``Publisher``, ``Book``, ``Version``
* ``Chapter``, ``ChapterContent``, ``Configuration``, ``RecommendedLanguages``

Friends protocols (``youversion.models.friends``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``Contact``, ``Contacts``, ``Friend``, ``Friends``
* ``FriendOffer``, ``Offers``, ``Friendable``, ``Friendables``

Events protocols (``youversion.models.events``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``Event``, ``EventContent``, ``EventLocation``, ``EventTime``
* ``SavedEvent``, ``SavedEvents``, ``SearchEvent``, ``SearchEvents``
* ``EventConfiguration``

Common API protocols (``youversion.models.common``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``UserBase``, ``Avatar``, ``Images``, ``Link``, ``Localize``
* ``ApiError``, ``ApiErrors``, ``ApiResponse``, ``PaginationInfo``

Verse of the day
~~~~~~~~~~~~~~~~

.. autoclass:: youversion.models.VotdProtocol
   :members:
   :no-index:

``Votd`` is a type alias for ``VotdProtocol``.

.. code-block:: python

   from youversion import SyncClient
   from youversion.models import Votd

   def day_label(votd: Votd) -> str:
       refs = votd.usfm or []
       return f"Day {votd.day}: {', '.join(refs)}"

   with SyncClient() as client:
       print(day_label(client.verse_of_the_day()))

Enums
-----

StatusEnum
~~~~~~~~~~

.. autoclass:: youversion.enums.StatusEnum
   :members:
   :no-index:

MomentKinds
~~~~~~~~~~~

.. autoclass:: youversion.enums.MomentKinds
   :members:
   :no-index:

``MomentKinds`` values include ``HIGHLIGHT``, ``NOTE``, ``IMAGE``, ``BOOKMARK``, ``FRIENDSHIP``, ``PLAN_SEGMENT_COMPLETION``, ``PLAN_SUBSCRIPTION``, and ``PLAN_COMPLETION``. Use them when building ``CreateMoment`` payloads, not when typing API responses.

Serialization
-------------

**Dynamic models** (API responses):

.. code-block:: python

   from youversion import SyncClient

   with SyncClient() as client:
       moment = client.highlights()[0]
       data = moment.model_dump()
       json_data = moment.model_dump_json()

**Static models** (request payloads):

.. code-block:: python

   from youversion.models.moments import CreateMoment

   payload = CreateMoment(...)  # see example above
   api_body = payload.model_dump()  # enums serialized to API string values

Package exports
---------------

``youversion.models`` re-exports protocols and static models. The top-level ``youversion`` package exports only ``AsyncClient`` and ``SyncClient`` — import model types from ``youversion.models`` or their submodules.
