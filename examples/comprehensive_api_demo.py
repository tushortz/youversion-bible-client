#!/usr/bin/env python3
"""
Comprehensive example demonstrating all YouVersion Bible API endpoints.

This script demonstrates how to use the updated YouVersion Bible client library
with all the new API endpoints extracted from the Android app.
"""

import asyncio
import json
from typing import Any, Dict

from youversion import AsyncClient


async def demonstrate_bible_api(client: AsyncClient):
    """Demonstrate Bible API endpoints."""
    print("=== Bible API Examples ===")

    # Get Bible configuration
    print("\n1. Getting Bible configuration...")
    config = await client.get_bible_configuration()
    print(f"Configuration: {json.dumps(config, indent=2)[:200]}...")

    # Get Bible versions for English
    print("\n2. Getting Bible versions for English...")
    versions = await client.get_bible_versions("eng", "all")
    if "response" in versions and "data" in versions["response"]:
        version_list = versions["response"]["data"].get("versions", [])
        print(f"Found {len(version_list)} versions")
        if version_list:
            first_version = version_list[0]
            print(
                f"First version: {first_version.get('title', 'Unknown')} ({first_version.get('abbreviation', 'N/A')})")

    # Get specific version details (using first version ID)
    if version_list:
        version_id = version_list[0]["id"]
        print(f"\n3. Getting details for version {version_id}...")
        version_details = await client.get_bible_version(version_id)
        print(
            f"Version details: {json.dumps(version_details, indent=2)[:200]}...")

    # Get recommended languages for US
    print("\n4. Getting recommended languages for US...")
    languages = await client.get_recommended_languages("US")
    print(f"Recommended languages: {json.dumps(languages, indent=2)[:200]}...")


async def demonstrate_search_api(client: AsyncClient):
    """Demonstrate Search API endpoints."""
    print("\n=== Search API Examples ===")

    # Search Bible text
    print("\n1. Searching Bible text for 'love'...")
    search_results = await client.search_bible("love", page=1)
    print(f"Search results: {json.dumps(search_results, indent=2)[:200]}...")

    # Search reading plans
    print("\n2. Searching reading plans for 'daily'...")
    plan_results = await client.search_plans("daily", "eng", page=1)
    print(
        f"Plan search results: {json.dumps(plan_results, indent=2)[:200]}...")


async def demonstrate_moments_api(client: AsyncClient):
    """Demonstrate Moments API endpoints."""
    print("\n=== Moments API Examples ===")

    # Get moments configuration
    print("\n1. Getting moments configuration...")
    config = await client.get_moments_configuration()
    print(f"Moments configuration: {json.dumps(config, indent=2)[:200]}...")

    # Get available highlight colors
    print("\n2. Getting available highlight colors...")
    colors = await client.get_moment_colors()
    print(f"Available colors: {json.dumps(colors, indent=2)[:200]}...")

    # Get moment labels
    print("\n3. Getting moment labels...")
    labels = await client.get_moment_labels()
    print(f"Moment labels: {json.dumps(labels, indent=2)[:200]}...")

    # Get verse of the day
    print("\n4. Getting verse of the day...")
    votd = await client.get_verse_of_the_day_new("eng")
    print(f"Verse of the day: {json.dumps(votd, indent=2)[:200]}...")


async def demonstrate_events_api(client: AsyncClient):
    """Demonstrate Events API endpoints."""
    print("\n=== Events API Examples ===")

    # Get event configuration
    print("\n1. Getting event configuration...")
    config = await client.get_event_configuration()
    print(f"Event configuration: {json.dumps(config, indent=2)[:200]}...")

    # Search events
    print("\n2. Searching events for 'church'...")
    events = await client.search_events("church", page=1)
    print(f"Event search results: {json.dumps(events, indent=2)[:200]}...")


async def demonstrate_videos_api(client: AsyncClient):
    """Demonstrate Videos API endpoints."""
    print("\n=== Videos API Examples ===")

    # Get videos list
    print("\n1. Getting videos list...")
    videos = await client.get_videos("eng")
    print(f"Videos: {json.dumps(videos, indent=2)[:200]}...")


async def demonstrate_themes_api(client: AsyncClient):
    """Demonstrate Themes API endpoints."""
    print("\n=== Themes API Examples ===")

    # Get available themes
    print("\n1. Getting available themes...")
    themes = await client.get_themes(page=1, language_tag="eng")
    print(f"Themes: {json.dumps(themes, indent=2)[:200]}...")


async def demonstrate_localization_api(client: AsyncClient):
    """Demonstrate Localization API endpoints."""
    print("\n=== Localization API Examples ===")

    # Get localization items
    print("\n1. Getting localization items for English...")
    localization = await client.get_localization_items("eng")
    print(f"Localization (first 200 chars): {localization[:200]}...")


async def main():
    """Main function to demonstrate all API endpoints."""
    print("YouVersion Bible API Comprehensive Demo")
    print("=" * 50)

    # Note: Most endpoints require authentication, but some public endpoints work without auth
    try:
        async with AsyncClient() as client:
            # Demonstrate public endpoints that don't require authentication
            await demonstrate_bible_api(client)
            await demonstrate_search_api(client)
            await demonstrate_moments_api(client)
            await demonstrate_events_api(client)
            await demonstrate_videos_api(client)
            await demonstrate_themes_api(client)
            await demonstrate_localization_api(client)

    except Exception as e:
        print(f"Error: {e}")
        print("Note: Some endpoints may require authentication.")
        print("To use authenticated endpoints, initialize the client with username and password:")
        print("async with AsyncClient(username='your_username', password='your_password') as client:")


if __name__ == "__main__":
    asyncio.run(main())
