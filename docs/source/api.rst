API Reference
=============

This section contains the API reference for the YouVersion Bible Client.

Overview
--------

The YouVersion Bible Client provides comprehensive access to the YouVersion API through two client implementations:

* **AsyncClient**: Asynchronous client for modern async/await code
* **SyncClient**: Synchronous wrapper around AsyncClient for traditional Python code

Both clients provide identical functionality with the same method signatures. The only difference is that AsyncClient methods are `async` and must be awaited.

Clients
-------

.. automodule:: youversion.clients
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

AsyncClient
~~~~~~~~~~~

The primary client for async applications. All methods are coroutines that must be awaited.

.. autoclass:: youversion.clients.AsyncClient
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

SyncClient
~~~~~~~~~~

Synchronous wrapper around AsyncClient. All methods are regular functions (not coroutines).

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

Bible Models
~~~~~~~~~~~~

.. automodule:: youversion.models.bible
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Friends Models
~~~~~~~~~~~~~~

.. automodule:: youversion.models.friends
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Events Models
~~~~~~~~~~~~~

.. automodule:: youversion.models.events
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

API Response Models
~~~~~~~~~~~~~~~~~~~

.. automodule:: youversion.models.common
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Moment Creation Models
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: youversion.models.moments
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Package Exports
~~~~~~~~~~~~~~~

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
