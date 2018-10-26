#!/usr/bin/env python3
"""
Synchronous vs Asynchronous Usage Examples

This example demonstrates the difference between using the synchronous Client
and the asynchronous AClient for the same operations.
"""

import asyncio
import time

from youversion.clients import AsyncClient, SyncClient


def sync_example():
    """Demonstrate synchronous usage"""
    print("🔄 SYNCHRONOUS USAGE")
    print("=" * 50)

    start_time = time.time()

    try:
        # Synchronous usage - no async/await needed
        with SyncClient() as client:
            print(f"✅ Connected as: {client.username}")

            # Get verse of the day
            votd = client.verse_of_the_day()
            print(f"📖 Verse of the day: {votd.usfm}")

            # Get highlights
            highlights = client.highlights(page=1)
            print(f"✨ Found {len(highlights)} highlights")

            # Get notes
            notes = client.notes(page=1)
            print(f"📝 Found {len(notes)} notes")

            # Get bookmarks
            bookmarks = client.bookmarks(page=1)
            print(f"🔖 Found {len(bookmarks)} bookmarks")

    except Exception as e:
        print(f"❌ Error: {e}")

    end_time = time.time()
    print(f"⏱️  Synchronous execution time: {end_time - start_time:.2f} seconds")


async def async_example():
    """Demonstrate asynchronous usage"""
    print("\n⚡ ASYNCHRONOUS USAGE")
    print("=" * 50)

    start_time = time.time()

    try:
        # Asynchronous usage - requires async/await
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")

            # Get verse of the day
            votd = await client.verse_of_the_day()
            print(f"📖 Verse of the day: {votd.usfm}")

            # Get highlights
            highlights = await client.highlights(page=1)
            print(f"✨ Found {len(highlights)} highlights")

            # Get notes
            notes = await client.notes(page=1)
            print(f"📝 Found {len(notes)} notes")

            # Get bookmarks
            bookmarks = await client.bookmarks(page=1)
            print(f"🔖 Found {len(bookmarks)} bookmarks")

    except Exception as e:
        print(f"❌ Error: {e}")

    end_time = time.time()
    print(f"⏱️  Asynchronous execution time: {end_time - start_time:.2f} seconds")


async def concurrent_example():
    """Demonstrate concurrent operations with async client"""
    print("\n🚀 CONCURRENT OPERATIONS")
    print("=" * 50)

    start_time = time.time()

    try:
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")

            # Run multiple operations concurrently
            votd_task = client.verse_of_the_day()
            highlights_task = client.highlights(page=1)
            notes_task = client.notes(page=1)
            bookmarks_task = client.bookmarks(page=1)

            # Wait for all tasks to complete
            votd, highlights, notes, bookmarks = await asyncio.gather(
                votd_task, highlights_task, notes_task, bookmarks_task
            )

            print(f"📖 Verse of the day: {votd.usfm}")
            print(f"✨ Found {len(highlights)} highlights")
            print(f"📝 Found {len(notes)} notes")
            print(f"🔖 Found {len(bookmarks)} bookmarks")

    except Exception as e:
        print(f"❌ Error: {e}")

    end_time = time.time()
    print(f"⏱️  Concurrent execution time: {end_time - start_time:.2f} seconds")


def main():
    """Main function demonstrating sync vs async usage"""
    print("🎯 YouVersion Bible Client - Sync vs Async Comparison")
    print("=" * 80)

    # Check credentials
    try:
        # Test credentials by creating a client
        test_client = SyncClient()
        print(f"✅ Credentials found for: {test_client.username}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Please set up your .env file with:")
        print("   YOUVERSION_USERNAME=your_username")
        print("   YOUVERSION_PASSWORD=your_password")
        return

    # Run synchronous example
    sync_example()

    # Run asynchronous example
    asyncio.run(async_example())

    # Run concurrent example
    asyncio.run(concurrent_example())

    print("\n📊 COMPARISON SUMMARY")
    print("=" * 50)
    print("🔄 Synchronous SyncClient:")
    print("   - Simple to use, no async/await needed")
    print("   - Good for simple scripts and sequential operations")
    print("   - Operations run one after another")
    print("   - Use: from youversion import SyncClient")

    print("\n⚡ Asynchronous AsyncClient:")
    print("   - Requires async/await syntax")
    print("   - Better for concurrent operations")
    print("   - Can run multiple operations simultaneously")
    print("   - Use: from youversion import AsyncClient")

    print("\n🚀 Concurrent Operations:")
    print("   - Best performance for multiple API calls")
    print("   - Use asyncio.gather() for parallel execution")
    print("   - Significantly faster for multiple operations")


if __name__ == "__main__":
    main()
