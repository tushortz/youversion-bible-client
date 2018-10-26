"""YouVersion Bible Client Library

A Python client library for accessing the YouVersion Bible API.
Supports both synchronous and asynchronous operations.

Example usage:

Synchronous:
    from youversion import SyncClient

    with SyncClient() as client:
        votd = client.verse_of_the_day()
        print(votd)

Asynchronous:
    import asyncio
    from youversion import AsyncClient

    async def main():
        async with AsyncClient() as client:
            votd = await client.verse_of_the_day()
            print(votd)

    asyncio.run(main())
"""

from .clients import AsyncClient, SyncClient

# Backward compatibility aliases
AClient = AsyncClient
Client = SyncClient

__version__ = "0.3.0"
__all__ = ["AsyncClient", "SyncClient", "AClient", "Client"]
