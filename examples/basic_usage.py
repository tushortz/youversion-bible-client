#!/usr/bin/env python3
"""
Complete API methods example for YouVersion Bible Client

This example demonstrates ALL public methods available in the Client class.
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
            print(f"  Day: {getattr(votd, 'day', 'N/A')}")
            print(f"  USFM: {getattr(votd, 'usfm', 'N/A')}")
            print(f"  Image ID: {getattr(votd, 'image_id', 'N/A')}")

            # Get specific day's verse
            votd_day_100 = client.verse_of_the_day(day=100)
            print("\nDay 100's verse:")
            print(f"  Day: {getattr(votd_day_100, 'day', 'N/A')}")
            print(f"  USFM: {getattr(votd_day_100, 'usfm', 'N/A')}")
            print(f"  Image ID: {getattr(votd_day_100, 'image_id', 'N/A')}")

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
        print(f"   Day: {getattr(votd, 'day', 'N/A')}")
        print(f"   USFM: {getattr(votd, 'usfm', 'N/A')}")
        print(f"   Image ID: {getattr(votd, 'image_id', 'N/A')}")

        # Get verse for a specific day (e.g., day 100)
        votd_specific = await client.verse_of_the_day(day=100)
        print("\n✅ Day 100 verse:")
        print(f"   Day: {getattr(votd_specific, 'day', 'N/A')}")
        print(f"   USFM: {getattr(votd_specific, 'usfm', 'N/A')}")
        print(f"   Image ID: {getattr(votd_specific, 'image_id', 'N/A')}")

    except Exception as e:
        print(f"❌ Error getting verse of the day: {e}")


async def demonstrate_moments(client: AsyncClient):
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
                moment_dict = (
                    moment.model_dump() if hasattr(moment, "model_dump") else {}
                )
                kind = moment_dict.get("kind_id") or getattr(
                    moment, "kind_id", "UNKNOWN"
                )
                title = moment_dict.get("moment_title") or getattr(
                    moment, "moment_title", "N/A"
                )
                moment_id = moment_dict.get("id") or getattr(moment, "id", "N/A")
                print(f"     {i+1}. Type: {kind}")
                print(f"        ID: {moment_id}")
                print(f"        Title: {title}")

        # Get second page
        moments_page2 = await client.moments(page=2)
        print(f"\n✅ Found {len(moments_page2)} moments on page 2")

    except Exception as e:
        print(f"❌ Error getting moments: {e}")


async def demonstrate_highlights(client: AsyncClient):
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
                highlight_dict = (
                    highlight.model_dump() if hasattr(highlight, "model_dump") else {}
                )
                title = highlight_dict.get("moment_title") or getattr(
                    highlight, "moment_title", "N/A"
                )
                highlight_id = highlight_dict.get("id") or getattr(
                    highlight, "id", "N/A"
                )
                references = highlight_dict.get("references") or getattr(
                    highlight, "references", []
                )
                print(f"     {i+1}. ID: {highlight_id}")
                print(f"        Title: {title}")
                print(f"        References: {len(references)}")

    except Exception as e:
        print(f"❌ Error getting highlights: {e}")


async def demonstrate_notes(client: AsyncClient):
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
                note_dict = note.model_dump() if hasattr(note, "model_dump") else {}
                title = note_dict.get("moment_title") or getattr(
                    note, "moment_title", "N/A"
                )
                content = note_dict.get("content") or getattr(note, "content", "N/A")
                note_id = note_dict.get("id") or getattr(note, "id", "N/A")
                status = note_dict.get("status") or getattr(note, "status", "N/A")
                print(f"     {i+1}. ID: {note_id}")
                print(f"        Title: {title}")
                content_preview = (
                    content[:100] + "..." if len(str(content)) > 100 else content
                )
                print(f"        Content: {content_preview}")
                print(f"        Status: {status}")

    except Exception as e:
        print(f"❌ Error getting notes: {e}")


async def demonstrate_bookmarks(client: AsyncClient):
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
                bookmark_dict = (
                    bookmark.model_dump() if hasattr(bookmark, "model_dump") else {}
                )
                title = bookmark_dict.get("moment_title") or getattr(
                    bookmark, "moment_title", "N/A"
                )
                bookmark_id = bookmark_dict.get("id") or getattr(bookmark, "id", "N/A")
                print(f"     {i+1}. ID: {bookmark_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting bookmarks: {e}")


async def demonstrate_my_images(client: AsyncClient):
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
                image_dict = image.model_dump() if hasattr(image, "model_dump") else {}
                title = image_dict.get("moment_title") or getattr(
                    image, "moment_title", "N/A"
                )
                image_id = image_dict.get("id") or getattr(image, "id", "N/A")
                print(f"     {i+1}. ID: {image_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting images: {e}")


async def demonstrate_badges(client: AsyncClient):
    """Demonstrate badges method"""
    print("\n🏅 BADGES")
    print("-" * 30)

    try:
        # Get first page of badges
        badges = await client.badges(page=1)
        print(f"✅ Found {len(badges)} badges on page 1")

        if badges:
            print("   First few badges:")
            for i, badge in enumerate(badges[:3]):
                badge_dict = badge.model_dump() if hasattr(badge, "model_dump") else {}
                title = badge_dict.get("moment_title") or getattr(
                    badge, "moment_title", "N/A"
                )
                badge_id = badge_dict.get("id") or getattr(badge, "id", "N/A")
                print(f"     {i+1}. ID: {badge_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting badges: {e}")


async def demonstrate_plan_progress(client: AsyncClient):
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
                progress_dict = (
                    progress.model_dump() if hasattr(progress, "model_dump") else {}
                )
                title = progress_dict.get("moment_title") or getattr(
                    progress, "moment_title", "N/A"
                )
                progress_id = progress_dict.get("id") or getattr(progress, "id", "N/A")
                print(f"     {i+1}. ID: {progress_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting plan progress: {e}")


async def demonstrate_plan_subscriptions(client: AsyncClient):
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
                sub_dict = sub.model_dump() if hasattr(sub, "model_dump") else {}
                title = sub_dict.get("moment_title") or getattr(
                    sub, "moment_title", "N/A"
                )
                sub_id = sub_dict.get("id") or getattr(sub, "id", "N/A")
                print(f"     {i+1}. ID: {sub_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting plan subscriptions: {e}")


async def demonstrate_plan_completions(client: AsyncClient):
    """Demonstrate plan_completions method"""
    print("\n✅ PLAN COMPLETIONS")
    print("-" * 30)

    try:
        # Get first page of plan completions
        completions = await client.plan_completions(page=1)
        print(f"✅ Found {len(completions)} plan completions on page 1")

        if completions:
            print("   First few plan completions:")
            for i, completion in enumerate(completions[:3]):
                completion_dict = (
                    completion.model_dump() if hasattr(completion, "model_dump") else {}
                )
                title = completion_dict.get("moment_title") or getattr(
                    completion, "moment_title", "N/A"
                )
                completion_id = completion_dict.get("id") or getattr(
                    completion, "id", "N/A"
                )
                print(f"     {i+1}. ID: {completion_id}")
                print(f"        Title: {title}")

    except Exception as e:
        print(f"❌ Error getting plan completions: {e}")


async def demonstrate_convert_note_to_md(client: AsyncClient):
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

    except Exception as e:
        print(f"❌ Error converting notes to markdown: {e}")


async def demonstrate_concurrent_usage(client: AsyncClient):
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
        if isinstance(votd, Exception):
            print(f"   Verse of the day: Error - {votd}")
        else:
            print(f"   Verse of the day: Day {getattr(votd, 'day', 'N/A')}")

        if isinstance(moments, Exception):
            print(f"   Moments: Error - {moments}")
        else:
            print(f"   Moments: {len(moments)}")

        if isinstance(highlights, Exception):
            print(f"   Highlights: Error - {highlights}")
        else:
            print(f"   Highlights: {len(highlights)}")

        if isinstance(notes, Exception):
            print(f"   Notes: Error - {notes}")
        else:
            print(f"   Notes: {len(notes)}")

        if isinstance(bookmarks, Exception):
            print(f"   Bookmarks: Error - {bookmarks}")
        else:
            print(f"   Bookmarks: {len(bookmarks)}")

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
            print(f"✅ User ID: {client.user_id}")

            # Demonstrate all public methods
            await demonstrate_verse_of_the_day(client)
            await demonstrate_moments(client)
            await demonstrate_highlights(client)
            await demonstrate_notes(client)
            await demonstrate_bookmarks(client)
            await demonstrate_my_images(client)
            await demonstrate_badges(client)
            await demonstrate_plan_progress(client)
            await demonstrate_plan_subscriptions(client)
            await demonstrate_plan_completions(client)
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
            print("   7. badges(page=1) - Get badges only")
            print("   8. plan_progress(page=1) - Get plan progress")
            print("   9. plan_subscriptions(page=1) - Get plan subscriptions")
            print("  10. plan_completions(page=1) - Get plan completions")
            print("  11. convert_note_to_md() - Convert notes to markdown")

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
