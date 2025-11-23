#!/usr/bin/env python3
"""
Comprehensive example demonstrating all YouVersion Bible API endpoints.

This script demonstrates how to use the YouVersion Bible client library
with all available API endpoints.
"""

import asyncio

from youversion.clients import AsyncClient


async def demonstrate_bible_api(client: AsyncClient):
    """Demonstrate Bible API endpoints."""
    print("=== Bible API Examples ===")

    # Get Bible configuration
    print("\n1. Getting Bible configuration...")
    config = await client.get_bible_configuration()
    print(f"Configuration type: {type(config)}")
    if hasattr(config, "model_dump"):
        print(f"Configuration keys: {list(config.model_dump().keys())[:5]}...")

    # Get Bible versions for English
    print("\n2. Getting Bible versions for English...")
    versions = await client.get_bible_versions("eng", "all")
    if isinstance(versions, dict):
        version_list = versions.get("versions", [])
        print(f"Found {len(version_list)} versions")
        if version_list:
            first_version = version_list[0]
            if isinstance(first_version, dict):
                print(f"First version: {first_version.get('title', 'Unknown')}")
    elif hasattr(versions, "versions"):
        print(
            f"Found versions: {len(versions.versions) if hasattr(versions.versions, '__len__') else 'N/A'}"
        )

    # Get specific version details
    print("\n3. Getting details for version 1...")
    version_details = await client.get_bible_version(1)
    print(f"Version details type: {type(version_details)}")

    # Get recommended languages for US
    print("\n4. Getting recommended languages for US...")
    languages = await client.get_recommended_languages("US")
    print(f"Languages type: {type(languages)}")

    # Get Bible chapter
    print("\n5. Getting Bible chapter GEN.1...")
    chapter = await client.get_bible_chapter("GEN.1", version_id=1)
    print(f"Chapter type: {type(chapter)}")


async def demonstrate_audio_api(client: AsyncClient):
    """Demonstrate Audio Bible API endpoints."""
    print("\n=== Audio Bible API Examples ===")

    # Get audio chapter
    print("\n1. Getting audio chapter GEN.1...")
    audio_chapter = await client.get_audio_chapter("GEN.1", version_id=1)
    print(f"Audio chapter type: {type(audio_chapter)}")

    # Get audio version
    print("\n2. Getting audio version 1...")
    audio_version = await client.get_audio_version(1)
    print(f"Audio version type: {type(audio_version)}")


async def demonstrate_search_api(client: AsyncClient):
    """Demonstrate Search API endpoints."""
    print("\n=== Search API Examples ===")

    # Search Bible text
    print("\n1. Searching Bible text for 'love'...")
    search_results = await client.search_bible("love", page=1)
    print(f"Search results type: {type(search_results)}")

    # Search reading plans
    print("\n2. Searching reading plans for 'daily'...")
    plan_results = await client.search_plans("daily", "en", page=1)
    print(f"Plan search results type: {type(plan_results)}")

    # Search users
    print("\n3. Searching users for 'john'...")
    user_results = await client.search_users("john", "eng", page=1)
    print(f"User search results type: {type(user_results)}")


async def demonstrate_moments_api(client: AsyncClient):
    """Demonstrate Moments API endpoints."""
    print("\n=== Moments API Examples ===")

    # Get moments configuration
    print("\n1. Getting moments configuration...")
    config = await client.get_moments_configuration()
    print(f"Moments configuration type: {type(config)}")

    # Get available highlight colors
    print("\n2. Getting available highlight colors...")
    colors = await client.get_moment_colors()
    print(f"Available colors type: {type(colors)}")

    # Get moment labels
    print("\n3. Getting moment labels...")
    labels = await client.get_moment_labels()
    print(f"Moment labels type: {type(labels)}")

    # Get verse of the day
    print("\n4. Getting verse of the day...")
    votd = await client.verse_of_the_day()
    print(f"Verse of the day: Day {getattr(votd, 'day', 'N/A')}")

    # Get moments list
    print("\n5. Getting moments list...")
    moments = await client.get_moments(page=1)
    print(f"Moments type: {type(moments)}")

    # Get verse colors
    print("\n6. Getting verse colors for GEN.1.1...")
    verse_colors = await client.get_verse_colors("GEN.1.1", version_id=1)
    print(f"Verse colors type: {type(verse_colors)}")


async def demonstrate_content_api(client: AsyncClient):
    """Demonstrate content retrieval endpoints."""
    print("\n=== Content API Examples ===")

    # Get moments
    print("\n1. Getting moments...")
    moments = await client.moments(page=1)
    print(f"Found {len(moments)} moments")

    # Get highlights
    print("\n2. Getting highlights...")
    highlights = await client.highlights(page=1)
    print(f"Found {len(highlights)} highlights")

    # Get notes
    print("\n3. Getting notes...")
    notes = await client.notes(page=1)
    print(f"Found {len(notes)} notes")

    # Get bookmarks
    print("\n4. Getting bookmarks...")
    bookmarks = await client.bookmarks(page=1)
    print(f"Found {len(bookmarks)} bookmarks")

    # Get badges
    print("\n5. Getting badges...")
    badges = await client.badges(page=1)
    print(f"Found {len(badges)} badges")

    # Get plan progress
    print("\n6. Getting plan progress...")
    progress = await client.plan_progress(page=1)
    print(f"Found {len(progress)} progress items")

    # Get plan subscriptions
    print("\n7. Getting plan subscriptions...")
    subscriptions = await client.plan_subscriptions(page=1)
    print(f"Found {len(subscriptions)} subscriptions")

    # Get plan completions
    print("\n8. Getting plan completions...")
    completions = await client.plan_completions(page=1)
    print(f"Found {len(completions)} completions")


async def demonstrate_events_api(client: AsyncClient):
    """Demonstrate Events API endpoints."""
    print("\n=== Events API Examples ===")

    # Get event configuration
    print("\n1. Getting event configuration...")
    config = await client.get_event_configuration()
    print(f"Event configuration type: {type(config)}")

    # Search events
    print("\n2. Searching events for 'church'...")
    events = await client.search_events("church", page=1)
    print(f"Event search results type: {type(events)}")

    # Get saved events
    print("\n3. Getting saved events...")
    saved_events = await client.get_saved_events(page=1)
    print(f"Saved events type: {type(saved_events)}")

    # Get all saved event IDs
    print("\n4. Getting all saved event IDs...")
    event_ids = await client.get_all_saved_event_ids()
    print(f"Event IDs type: {type(event_ids)}")


async def demonstrate_videos_api(client: AsyncClient):
    """Demonstrate Videos API endpoints."""
    print("\n=== Videos API Examples ===")

    # Get videos list
    print("\n1. Getting videos list...")
    videos = await client.get_videos("eng")
    print(f"Videos type: {type(videos)}")

    # Get video details (if we have a video ID)
    print("\n2. Getting video details (example with ID 1)...")
    try:
        video = await client.get_video_details(1)
        print(f"Video details type: {type(video)}")
    except Exception as e:
        print(f"Note: Video may not exist - {e}")


async def demonstrate_images_api(client: AsyncClient):
    """Demonstrate Images API endpoints."""
    print("\n=== Images API Examples ===")

    # Get images for a reference
    print("\n1. Getting images for GEN.1.1...")
    images = await client.get_images("GEN.1.1", "eng", page=1)
    print(f"Images type: {type(images)}")

    # Get image upload URL
    print("\n2. Getting image upload URL...")
    upload_url = await client.get_image_upload_url()
    print(f"Upload URL type: {type(upload_url)}")


async def demonstrate_themes_api(client: AsyncClient):
    """Demonstrate Themes API endpoints."""
    print("\n=== Themes API Examples ===")

    # Get available themes
    print("\n1. Getting available themes...")
    themes = await client.get_themes(page=1, language_tag="eng")
    print(f"Themes type: {type(themes)}")

    # Get theme description (if we have a theme ID)
    print("\n2. Getting theme description (example with ID 1)...")
    try:
        description = await client.get_theme_description(1, "eng")
        print(f"Theme description type: {type(description)}")
    except Exception as e:
        print(f"Note: Theme may not exist - {e}")


async def demonstrate_localization_api(client: AsyncClient):
    """Demonstrate Localization API endpoints."""
    print("\n=== Localization API Examples ===")

    # Get localization items
    print("\n1. Getting localization items for English...")
    localization = await client.get_localization_items("eng")
    print(f"Localization type: {type(localization)}")
    print(
        f"Localization length: {len(localization) if isinstance(localization, str) else 'N/A'}"
    )


async def main():
    """Main function to demonstrate all API endpoints."""
    print("YouVersion Bible API Comprehensive Demo")
    print("=" * 50)

    # Note: Most endpoints require authentication
    try:
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")
            print(f"✅ User ID: {client.user_id}")
            print()

            # Demonstrate all API categories
            await demonstrate_bible_api(client)
            await demonstrate_audio_api(client)
            await demonstrate_search_api(client)
            await demonstrate_moments_api(client)
            await demonstrate_content_api(client)
            await demonstrate_events_api(client)
            await demonstrate_videos_api(client)
            await demonstrate_images_api(client)
            await demonstrate_themes_api(client)
            await demonstrate_localization_api(client)

            print("\n✅ Comprehensive demo completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Note: Some endpoints may require authentication.")
        print(
            "To use authenticated endpoints, initialize the client with username and password:"
        )
        print(
            "async with AsyncClient(username='your_username', password='your_password') as client:"
        )


if __name__ == "__main__":
    asyncio.run(main())
