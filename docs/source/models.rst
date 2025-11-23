Data Models
===========

The YouVersion Bible Client uses Pydantic models for type-safe data handling and validation.

Core Models
-----------

Votd
~~~~

Verse of the day model.

.. class:: Votd

   .. attribute:: day: int

      Day number (1-365)

   .. attribute:: usfm: List[str]

      USFM references for the verse

   .. attribute:: image_id: Optional[str]

      Associated image ID

.. code-block:: python

   from youversion import Votd

   votd = Votd(day=1, usfm=["JHN.3.16"], image_id="img123")
   print(f"Day {votd.day}: {votd.usfm}")

Moment
~~~~~~

Base model for all YouVersion moment objects.

.. class:: Moment

   .. attribute:: id: str

      Unique moment identifier

   .. attribute:: kind: str

      Type of moment (e.g., "highlight", "note", "image")

   .. attribute:: moment_title: str

      Title of the moment

   .. attribute:: time_ago: str

      Human-readable time since creation

   .. attribute:: owned_by_me: bool

      Whether the moment is owned by the current user

   .. attribute:: created_dt: Optional[datetime]

      Creation datetime

   .. attribute:: updated_dt: Optional[datetime]

      Last update datetime

   .. attribute:: user: User

      User who created the moment

   .. attribute:: actions: Action

      Available actions for the moment

   .. attribute:: comments: Comment

      Comment information

   .. attribute:: likes: Like

      Like information

   .. attribute:: avatar: str

      Avatar URL

   .. attribute:: path: str

      Full URL path to the moment

Highlight
~~~~~~~~~

Model for Bible verse highlights.

.. class:: Highlight(Moment)

   .. attribute:: references: List[Reference]

      Bible verse references

   .. attribute:: text: Optional[str]

      Highlighted text content

.. code-block:: python

   from youversion import Highlight

   highlight = Highlight(
       id="123",
       kind="highlight",
       moment_title="John 3:16",
       references=[Reference(version_id=1, human="John 3:16", usfm="JHN.3.16")],
       text="For God so loved the world..."
   )

Note
~~~~

Model for Bible study notes.

.. class:: Note(Moment)

   .. attribute:: content: str

      Note content

   .. attribute:: references: List[Reference]

      Related Bible verse references

   .. attribute:: status: StatusEnum

      Note status (PRIVATE, PUBLIC, etc.)

.. code-block:: python

   from youversion import Note, StatusEnum

   note = Note(
       id="456",
       kind="note",
       moment_title="Study Notes",
       content="This verse teaches us about God's love",
       references=[Reference(version_id=1, human="John 3:16", usfm="JHN.3.16")],
       status=StatusEnum.PRIVATE
   )

Image
~~~~~

Model for shared Bible images.

.. class:: Image(Moment)

   .. attribute:: references: List[Reference]

      Related Bible verse references

   .. attribute:: body_image: str

      Image URL

   .. attribute:: action_url: Optional[str]

      Action URL for the image

Friendship
~~~~~~~~~~

Model for friendship moments.

.. class:: Friendship(Moment)

   .. attribute:: friend_name: str

      Friend's name

   .. attribute:: friend_path: str

      Friend's profile path

   .. attribute:: friend_avatar: str

      Friend's avatar URL

Plan Models
-----------

PlanSegmentCompletion
~~~~~~~~~~~~~~~~~~~~~

Model for reading plan segment completions.

.. class:: PlanSegmentCompletion(PlanModel)

   .. attribute:: percent_complete: float

      Completion percentage (0.0-1.0)

   .. attribute:: segment: int

      Segment number

   .. attribute:: total_segments: int

      Total segments in the plan

   .. attribute:: plan_id: int

      Plan identifier

   .. attribute:: subscribed: bool

      Whether the user is subscribed to the plan

PlanSubscription
~~~~~~~~~~~~~~~~

Model for reading plan subscriptions.

.. class:: PlanSubscription(PlanModel)

   .. attribute:: plan_title: str

      Title of the subscribed plan

   .. attribute:: plan_id: int

      Plan identifier

   .. attribute:: subscribed: bool

      Whether the user is subscribed to the plan

PlanCompletion
~~~~~~~~~~~~~~

Model for completed reading plans.

.. class:: PlanCompletion(PlanModel)

   .. attribute:: plan_title: str

      Title of the completed plan

   .. attribute:: plan_id: int

      Plan identifier

   .. attribute:: subscribed: bool

      Whether the user is subscribed to the plan

Supporting Models
-----------------

Reference
~~~~~~~~~

Model for Bible verse references.

.. class:: Reference

   .. attribute:: version_id: Union[str, int]

      Bible version identifier

   .. attribute:: human: str

      Human-readable reference (e.g., "John 3:16")

   .. attribute:: usfm: Union[str, List[str]]

      USFM reference format

User
~~~~

Model for YouVersion users.

.. class:: User

   .. attribute:: id: Optional[Union[str, int]]

      User identifier

   .. attribute:: path: str

      User profile path

   .. attribute:: user_name: Optional[str]

      Username

Action
~~~~~~

Model for moment actions.

.. class:: Action

   .. attribute:: deletable: bool

      Whether the moment can be deleted

   .. attribute:: editable: bool

      Whether the moment can be edited

   .. attribute:: read: bool

      Whether the moment can be read

   .. attribute:: show: bool

      Whether the moment should be shown

Comment
~~~~~~~

Model for comment information.

.. class:: Comment(ReactionModel)

   .. attribute:: enabled: bool

      Whether comments are enabled

   .. attribute:: count: int

      Number of comments

   .. attribute:: strings: Dict[str, Any]

      Comment-related strings

   .. attribute:: all: List[Any]

      All comment data

Like
~~~

Model for like information.

.. class:: Like(ReactionModel)

   .. attribute:: enabled: bool

      Whether likes are enabled

   .. attribute:: count: int

      Number of likes

   .. attribute:: strings: Dict[str, Any]

      Like-related strings

   .. attribute:: all: List[Any]

      All like data

   .. attribute:: is_liked: bool

      Whether the current user has liked the moment

   .. attribute:: user_ids: Optional[List[int]]

      List of user IDs who liked the moment

Enums
-----

StatusEnum
~~~~~~~~~~

Enumeration for note status values.

.. class:: StatusEnum

   .. attribute:: PRIVATE

      Private note

   .. attribute:: PUBLIC

      Public note

MomentKinds
~~~~~~~~~~~

Enumeration for moment types.

.. class:: MomentKinds

   .. attribute:: HIGHLIGHT

      Highlight moment

   .. attribute:: NOTE

      Note moment

   .. attribute:: IMAGE

      Image moment

   .. attribute:: FRIENDSHIP

      Friendship moment

   .. attribute:: PLAN_SEGMENT_COMPLETION

      Plan segment completion

   .. attribute:: PLAN_COMPLETION

      Plan completion

   .. attribute:: PLAN_SUBSCRIPTION

      Plan subscription

Model Validation
----------------

All models use Pydantic for automatic validation and serialization:

.. code-block:: python

   from youversion import Highlight
   from pydantic import ValidationError

   try:
       highlight = Highlight(
           id="123",
           kind="highlight",
           moment_title="Test",
           # Missing required fields will raise ValidationError
       )
   except ValidationError as e:
       print(f"Validation error: {e}")

Model Serialization
-------------------

Models can be serialized to dictionaries and JSON:

.. code-block:: python

   from youversion import Votd

   votd = Votd(day=1, usfm=["JHN.3.16"], image_id="img123")

   # Convert to dictionary
   data = votd.model_dump()
   print(data)

   # Convert to JSON
   json_data = votd.model_dump_json()
   print(json_data)

   # Convert with exclusions
   minimal_data = votd.model_dump(exclude={'image_id'})
   print(minimal_data)
