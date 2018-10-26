#!/usr/bin/env python3
"""
Complete API methods example for YouVersion Bible Client

This example demonstrates ALL public methods available in the Client class:
1. verse_of_the_day() - Get verse of the day (current or specific day)
2. moments() - Get all moments (friendships, highlights, notes, images, etc.)
3. highlights() - Get highlights only
4. notes() - Get notes only
5. bookmarks() - Get bookmarks only
6. my_images() - Get images only
7. plan_progress() - Get plan progress/segment completion
8. plan_subscriptions() - Get plan subscriptions
9. convert_note_to_md() - Convert notes to markdown format

Make sure to set up your .env file with YOUVERSION_USERNAME and YOUVERSION_PASSWORD
or pass credentials directly to the Client constructor.
"""

import asyncio
import os

from youversion.clients import AsyncClient, SyncClient


def demonstrate_sync_verse_of_the_day():
    """Demonstrate synchronous verse_of_the_day method"""
    print("\n📖 SYNC VERSE OF THE DAY")
    print("=" * 50)

    try:
        # Synchronous usage - no async/await needed
        with SyncClient() as client:
            # Get current day's verse
            votd = client.verse_of_the_day()
            print("Current day's verse:")
            print(f"  Day: {votd.day}")
            print(f"  USFM: {votd.usfm}")
            print(f"  Image ID: {votd.image_id}")

            # Get specific day's verse
            votd_day_100 = client.verse_of_the_day(day=100)
            print("\nDay 100's verse:")
            print(f"  Day: {votd_day_100.day}")
            print(f"  USFM: {votd_day_100.usfm}")
            print(f"  Image ID: {votd_day_100.image_id}")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demonstrate_verse_of_the_day(client: AsyncClient):
    """Demonstrate verse_of_the_day method"""
    print("\n📖 VERSE OF THE DAY")
    print("-" * 30)

    try:
        # Get current day's verse
        votd = await client.verse_of_the_day()
        print("✅ Current day verse:")
        print(f"   Day: {votd.day}")
        print(f"   USFM: {votd.usfm}")
        print(f"   Image ID: {votd.image_id}")

        # Get verse for a specific day (e.g., day 100)
        votd_specific = await client.verse_of_the_day(day=100)
        print("\n✅ Day 100 verse:")
        print(f"   Day: {votd_specific.day}")
        print(f"   USFM: {votd_specific.usfm}")
        print(f"   Image ID: {votd_specific.image_id}")

    except Exception as e:
        print(f"❌ Error getting verse of the day: {e}")


async def demonstrate_moments(client: Client):
    """Demonstrate moments method"""
    print("\n📋 MOMENTS")
    print("-" * 30)

    try:
        # Get first page of moments
        moments = await client.moments(page=1)
        print(f"✅ Found {len(moments)} moments on page 1")

        if moments:
            print("   First few moments:")
            for i, moment in enumerate(moments[:3]):
                print(f"     {i+1}. Type: {moment.kind}")
                print(f"        Title: {moment.moment_title}")
                print(f"        Time: {moment.time_ago}")
                print(f"        Owned by me: {moment.owned_by_me}")

        # Get second page
        moments_page2 = await client.moments(page=2)
        print(f"\n✅ Found {len(moments_page2)} moments on page 2")

    except Exception as e:
        print(f"❌ Error getting moments: {e}")


async def demonstrate_highlights(client: Client):
    """Demonstrate highlights method"""
    print("\n✨ HIGHLIGHTS")
    print("-" * 30)

    try:
        # Get first page of highlights
        highlights = await client.highlights(page=1)
        print(f"✅ Found {len(highlights)} highlights on page 1")

        if highlights:
            print("   First few highlights:")
            for i, highlight in enumerate(highlights[:3]):
                print(f"     {i+1}. Title: {highlight.moment_title}")
                print(f"        References: {len(highlight.references)}")
                print(f"        Time: {highlight.time_ago}")
                if highlight.references:
                    print(f"        First reference: {highlight.references[0].human}")

        # Get second page
        highlights_page2 = await client.highlights(page=2)
        print(f"\n✅ Found {len(highlights_page2)} highlights on page 2")

    except Exception as e:
        print(f"❌ Error getting highlights: {e}")


async def demonstrate_notes(client: Client):
    """Demonstrate notes method"""
    print("\n📝 NOTES")
    print("-" * 30)

    try:
        # Get first page of notes
        notes = await client.notes(page=1)
        print(f"✅ Found {len(notes)} notes on page 1")

        if notes:
            print("   First few notes:")
            for i, note in enumerate(notes[:3]):
                print(f"     {i+1}. Title: {note.moment_title}")
                print(
                    f"        Content: {note.content[:100]}..."
                    if len(note.content) > 100
                    else f"        Content: {note.content}"
                )
                print(f"        Status: {note.status}")
                print(f"        References: {len(note.references)}")
                print(f"        Time: {note.time_ago}")

        # Get second page
        notes_page2 = await client.notes(page=2)
        print(f"\n✅ Found {len(notes_page2)} notes on page 2")

    except Exception as e:
        print(f"❌ Error getting notes: {e}")


async def demonstrate_bookmarks(client: Client):
    """Demonstrate bookmarks method"""
    print("\n🔖 BOOKMARKS")
    print("-" * 30)

    try:
        # Get first page of bookmarks
        bookmarks = await client.bookmarks(page=1)
        print(f"✅ Found {len(bookmarks)} bookmarks on page 1")

        if bookmarks:
            print("   First few bookmarks:")
            for i, bookmark in enumerate(bookmarks[:3]):
                print(f"     {i+1}. Title: {bookmark.get('moment_title', 'N/A')}")
                print(f"        Kind: {bookmark.get('kind', 'N/A')}")
                print(f"        Time: {bookmark.get('time_ago', 'N/A')}")

        # Get second page
        bookmarks_page2 = await client.bookmarks(page=2)
        print(f"\n✅ Found {len(bookmarks_page2)} bookmarks on page 2")

    except Exception as e:
        print(f"❌ Error getting bookmarks: {e}")


async def demonstrate_my_images(client: Client):
    """Demonstrate my_images method"""
    print("\n🖼️  MY IMAGES")
    print("-" * 30)

    try:
        # Get first page of images
        images = await client.my_images(page=1)
        print(f"✅ Found {len(images)} images on page 1")

        if images:
            print("   First few images:")
            for i, image in enumerate(images[:3]):
                print(f"     {i+1}. Title: {image.get('moment_title', 'N/A')}")
                print(f"        Kind: {image.get('kind', 'N/A')}")
                print(f"        Time: {image.get('time_ago', 'N/A')}")
                if "body_image" in image:
                    print(f"        Body image: {image['body_image'][:50]}...")

        # Get second page
        images_page2 = await client.my_images(page=2)
        print(f"\n✅ Found {len(images_page2)} images on page 2")

    except Exception as e:
        print(f"❌ Error getting images: {e}")


async def demonstrate_plan_progress(client: Client):
    """Demonstrate plan_progress method"""
    print("\n📊 PLAN PROGRESS")
    print("-" * 30)

    try:
        # Get first page of plan progress
        plan_progress = await client.plan_progress(page=1)
        print(f"✅ Found {len(plan_progress)} plan progress items on page 1")

        if plan_progress:
            print("   First few plan progress items:")
            for i, progress in enumerate(plan_progress[:3]):
                print(f"     {i+1}. Title: {progress.get('moment_title', 'N/A')}")
                print(f"        Kind: {progress.get('kind', 'N/A')}")
                print(f"        Time: {progress.get('time_ago', 'N/A')}")
                if "percent_complete" in progress:
                    print(f"        Progress: {progress['percent_complete']}%")

        # Get second page
        plan_progress_page2 = await client.plan_progress(page=2)
        print(f"\n✅ Found {len(plan_progress_page2)} plan progress items on page 2")

    except Exception as e:
        print(f"❌ Error getting plan progress: {e}")


async def demonstrate_plan_subscriptions(client: Client):
    """Demonstrate plan_subscriptions method"""
    print("\n📅 PLAN SUBSCRIPTIONS")
    print("-" * 30)

    try:
        # Get first page of plan subscriptions
        plan_subs = await client.plan_subscriptions(page=1)
        print(f"✅ Found {len(plan_subs)} plan subscriptions on page 1")

        if plan_subs:
            print("   First few plan subscriptions:")
            for i, sub in enumerate(plan_subs[:3]):
                print(f"     {i+1}. Title: {sub.get('moment_title', 'N/A')}")
                print(f"        Kind: {sub.get('kind', 'N/A')}")
                print(f"        Time: {sub.get('time_ago', 'N/A')}")
                if "plan_title" in sub:
                    print(f"        Plan: {sub['plan_title']}")

        # Get second page
        plan_subs_page2 = await client.plan_subscriptions(page=2)
        print(f"\n✅ Found {len(plan_subs_page2)} plan subscriptions on page 2")

    except Exception as e:
        print(f"❌ Error getting plan subscriptions: {e}")


async def demonstrate_convert_note_to_md(client: Client):
    """Demonstrate convert_note_to_md method"""
    print("\n📄 CONVERT NOTE TO MARKDOWN")
    print("-" * 30)

    try:
        # Convert notes to markdown
        notes_md = await client.convert_note_to_md()
        print(f"✅ Converted {len(notes_md)} notes to markdown")

        if notes_md:
            print("   Note data structure:")
            print(f"     Type: {type(notes_md)}")
            print(f"     Length: {len(notes_md)}")
            if notes_md:
                print(
                    f"     First note keys: {list(notes_md[0].keys()) if isinstance(notes_md[0], dict) else 'Not a dict'}"
                )

    except Exception as e:
        print(f"❌ Error converting notes to markdown: {e}")


async def demonstrate_concurrent_usage(client: Client):
    """Demonstrate using multiple methods concurrently"""
    print("\n🚀 CONCURRENT USAGE")
    print("-" * 30)

    try:
        # Run multiple methods concurrently
        results = await asyncio.gather(
            client.verse_of_the_day(),
            client.moments(page=1),
            client.highlights(page=1),
            client.notes(page=1),
            client.bookmarks(page=1),
            return_exceptions=True,
        )

        votd, moments, highlights, notes, bookmarks = results

        print("✅ Concurrent results:")
        print(
            f"   Verse of the day: Day {votd.day if not isinstance(votd, Exception) else 'Error'}"
        )
        print(
            f"   Moments: {len(moments) if not isinstance(moments, Exception) else 'Error'}"
        )
        print(
            f"   Highlights: {len(highlights) if not isinstance(highlights, Exception) else 'Error'}"
        )
        print(
            f"   Notes: {len(notes) if not isinstance(notes, Exception) else 'Error'}"
        )
        print(
            f"   Bookmarks: {len(bookmarks) if not isinstance(bookmarks, Exception) else 'Error'}"
        )

    except Exception as e:
        print(f"❌ Error in concurrent usage: {e}")


async def main():
    """Main function demonstrating all API methods"""

    # Check if credentials are available
    username = os.getenv("YOUVERSION_USERNAME")
    password = os.getenv("YOUVERSION_PASSWORD")

    if not username or not password:
        print(
            "❌ Error: Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables"
        )
        print("   Or create a .env file with your credentials")
        print("   Example:")
        print("   YOUVERSION_USERNAME=your_username")
        print("   YOUVERSION_PASSWORD=your_password")
        return

    print("🚀 Starting YouVersion Bible Client - Complete API Methods Example")
    print("=" * 80)

    try:
        # Initialize client with environment variables
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")

            # Demonstrate all public methods
            await demonstrate_verse_of_the_day(client)
            await demonstrate_moments(client)
            await demonstrate_highlights(client)
            await demonstrate_notes(client)
            await demonstrate_bookmarks(client)
            await demonstrate_my_images(client)
            await demonstrate_plan_progress(client)
            await demonstrate_plan_subscriptions(client)
            await demonstrate_convert_note_to_md(client)
            await demonstrate_concurrent_usage(client)

            print("\n✅ Complete API methods example completed successfully!")
            print("\n📋 Summary of all public methods demonstrated:")
            print("   1. verse_of_the_day(day=None) - Get verse of the day")
            print("   2. moments(page=1) - Get all moments")
            print("   3. highlights(page=1) - Get highlights only")
            print("   4. notes(page=1) - Get notes only")
            print("   5. bookmarks(page=1) - Get bookmarks only")
            print("   6. my_images(page=1) - Get images only")
            print("   7. plan_progress(page=1) - Get plan progress")
            print("   8. plan_subscriptions(page=1) - Get plan subscriptions")
            print("   9. convert_note_to_md() - Convert notes to markdown")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   This might be due to:")
        print("   - Invalid credentials")
        print("   - Network connectivity issues")
        print("   - YouVersion API changes")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
