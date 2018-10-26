API Reference
=============

This section contains the complete API reference for the YouVersion Bible Client.

Clients
-------

.. automodule:: youversion.clients
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

AsyncClient
~~~~~~~~~~~

.. autoclass:: youversion.clients.AsyncClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

SyncClient
~~~~~~~~~~

.. autoclass:: youversion.clients.SyncClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Core Components
---------------

Authenticator
~~~~~~~~~~~~~

.. automodule:: youversion.core.authenticator
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.authenticator.Authenticator
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

HttpClient
~~~~~~~~~~

.. automodule:: youversion.core.http_client
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.http_client.HttpClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

DataProcessor
~~~~~~~~~~~~~

.. automodule:: youversion.core.data_processor
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.data_processor.DataProcessor
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

URLDiscovery
~~~~~~~~~~~~

.. automodule:: youversion.core.url_discovery
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.url_discovery.URLDiscovery
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

BaseClient
~~~~~~~~~~

.. automodule:: youversion.core.base_client
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.base_client.BaseClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Data Models
-----------

Base Models
~~~~~~~~~~~

.. automodule:: youversion.models.base
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.base.Moment
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.base.PlanModel
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.base.Reference
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Common Models
~~~~~~~~~~~~~

.. automodule:: youversion.models.commons
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.commons.User
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.commons.Action
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.commons.Comment
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.commons.Like
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.commons.BodyImage
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Main Models
~~~~~~~~~~~

.. automodule:: youversion.models
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.Votd
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.Highlight
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.Note
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.Image
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.Friendship
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.PlanSegmentCompletion
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.PlanSubscription
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.models.PlanCompletion
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Enums
-----

.. automodule:: youversion.enums
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.enums.StatusEnum
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.enums.MomentKinds
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Configuration
-------------

.. automodule:: youversion.config
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.config.Config
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

CLI
---

.. automodule:: youversion.cli
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Interfaces
----------

.. automodule:: youversion.core.interfaces
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.interfaces.IAuthenticator
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.interfaces.IHttpClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.interfaces.IDataProcessor
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: youversion.core.interfaces.IClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
