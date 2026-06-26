#!/usr/bin/env python3
"""Synchronous vs asynchronous usage examples."""

import asyncio
import time

from youversion.clients import AsyncClient, SyncClient


def sync_example():
    """Demonstrate synchronous usage."""
    print("SYNCHRONOUS USAGE")
    print("=" * 50)

    start_time = time.time()
    try:
        with SyncClient() as client:
            print(f"Connected as: {client.username}")
            votd = client.verse_of_the_day()
            print(f"Verse of the day: {votd.usfm}")
            print(f"Highlights: {len(client.highlights(page=1))}")
            print(f"Notes: {len(client.notes(page=1))}")
            print(f"Bookmarks: {len(client.bookmarks(page=1))}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Synchronous time: {time.time() - start_time:.2f}s")


async def async_example():
    """Demonstrate asynchronous usage."""
    print("\nASYNCHRONOUS USAGE")
    print("=" * 50)

    start_time = time.time()
    try:
        async with AsyncClient() as client:
            print(f"Connected as: {client.username}")
            votd = await client.verse_of_the_day()
            print(f"Verse of the day: {votd.usfm}")
            print(f"Highlights: {len(await client.highlights(page=1))}")
            print(f"Notes: {len(await client.notes(page=1))}")
            print(f"Bookmarks: {len(await client.bookmarks(page=1))}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Asynchronous time: {time.time() - start_time:.2f}s")


async def concurrent_example():
    """Run multiple calls in parallel."""
    print("\nCONCURRENT OPERATIONS")
    print("=" * 50)

    start_time = time.time()
    try:
        async with AsyncClient() as client:
            votd, highlights, notes, bookmarks = await asyncio.gather(
                client.verse_of_the_day(),
                client.highlights(page=1),
                client.notes(page=1),
                client.bookmarks(page=1),
            )
            print(f"Verse of the day: {votd.usfm}")
            print(f"Highlights: {len(highlights)}")
            print(f"Notes: {len(notes)}")
            print(f"Bookmarks: {len(bookmarks)}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Concurrent time: {time.time() - start_time:.2f}s")


def main():
    print("YouVersion Bible Client - Sync vs Async")
    print("=" * 80)

    try:
        test_client = SyncClient()
        print(f"Credentials found for: {test_client.username}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set YOUVERSION_USERNAME and YOUVERSION_PASSWORD in .env")
        return

    sync_example()
    asyncio.run(async_example())
    asyncio.run(concurrent_example())


if __name__ == "__main__":
    main()
