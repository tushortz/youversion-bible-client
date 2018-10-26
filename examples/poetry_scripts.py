#!/usr/bin/env python3
"""
Poetry Script Commands Example

This example demonstrates how to use the Poetry script commands
that are available after installing the package with Poetry.

Note: These commands are designed to be run from the command line using:
    poetry run yv-votd
    poetry run yv-moments
    etc.

This file shows the equivalent Python code for each command.
"""

import asyncio

from youversion.clients import AsyncClient


async def demonstrate_poetry_commands():
    """Demonstrate the equivalent of Poetry script commands"""
    print("🎯 YouVersion Bible Client - Poetry Script Commands Demo")
    print("=" * 80)
    print("These are the Python equivalents of the Poetry script commands:")
    print()

    try:
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")
            print()

            # Equivalent of: poetry run votd
            print("📖 poetry run votd")
            print("-" * 30)
            votd = await client.verse_of_the_day()
            print(f"Day: {votd.day}")
            print(f"USFM: {votd.usfm}")
            print(f"Image ID: {votd.image_id}")
            print()

            # Equivalent of: poetry run moments
            print("📝 poetry run moments")
            print("-" * 30)
            try:
                moments = await client.moments(page=1)
                print(f"Found {len(moments)} moments")
                if moments:
                    print(f"First moment type: {moments[0].__class__.__name__}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run highlights
            print("✨ poetry run highlights")
            print("-" * 30)
            try:
                highlights = await client.highlights(page=1)
                print(f"Found {len(highlights)} highlights")
                if highlights:
                    print(f"First highlight type: {highlights[0].__class__.__name__}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run notes
            print("📄 poetry run notes")
            print("-" * 30)
            try:
                notes = await client.notes(page=1)
                print(f"Found {len(notes)} notes")
                if notes:
                    print(f"First note type: {type(notes[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run bookmarks
            print("🔖 poetry run bookmarks")
            print("-" * 30)
            try:
                bookmarks = await client.bookmarks(page=1)
                print(f"Found {len(bookmarks)} bookmarks")
                if bookmarks:
                    print(f"First bookmark type: {type(bookmarks[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run images
            print("🖼️ poetry run images")
            print("-" * 30)
            try:
                images = await client.my_images(page=1)
                print(f"Found {len(images)} images")
                if images:
                    print(f"First image type: {type(images[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run plan-progress
            print("📊 poetry run plan-progress")
            print("-" * 30)
            try:
                progress = await client.plan_progress(page=1)
                print(f"Found {len(progress)} progress items")
                if progress:
                    print(f"First progress type: {type(progress[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run plan-subscriptions
            print("📋 poetry run plan-subscriptions")
            print("-" * 30)
            try:
                subscriptions = await client.plan_subscriptions(page=1)
                print(f"Found {len(subscriptions)} subscriptions")
                if subscriptions:
                    print(f"First subscription type: {type(subscriptions[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            # Equivalent of: poetry run convert-notes
            print("🔄 poetry run convert-notes")
            print("-" * 30)
            try:
                converted = await client.convert_note_to_md()
                print(f"Converted {len(converted)} notes")
                if converted:
                    print(f"First converted type: {type(converted[0])}")
            except Exception as e:
                print(f"Error: {e}")
            print()

            print("✅ Poetry script commands demo completed!")
            print()
            print("💡 To use these commands from the command line:")
            print("   poetry run votd")
            print("   poetry run moments")
            print("   poetry run highlights")
            print("   poetry run notes")
            print("   poetry run bookmarks")
            print("   poetry run images")
            print("   poetry run plan-progress")
            print("   poetry run plan-subscriptions")
            print("   poetry run convert-notes")
            print()
            print("💡 To use the main CLI with arguments:")
            print("   poetry run youversion votd --day 100")
            print("   poetry run youversion moments --page 2 --limit 5")
            print("   poetry run youversion highlights --json")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure you have set up your .env file with:")
        print("   YOUVERSION_USERNAME=your_username")
        print("   YOUVERSION_PASSWORD=your_password")


if __name__ == "__main__":
    asyncio.run(demonstrate_poetry_commands())
