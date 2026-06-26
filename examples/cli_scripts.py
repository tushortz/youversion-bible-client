#!/usr/bin/env python3
"""
CLI script entry points example.

After `uv sync`, these commands are available as console scripts:
    uv run votd
    uv run moments
    etc.

This file shows the equivalent Python API calls.
"""

import asyncio

from youversion.clients import AsyncClient


async def demonstrate_cli_commands():
    """Demonstrate the equivalent of console script commands."""
    print("YouVersion Bible Client - CLI Scripts Demo")
    print("=" * 80)
    print("Python equivalents of `uv run <command>`:")
    print()

    try:
        async with AsyncClient() as client:
            print(f"Connected as: {client.username}")
            print()

            print("uv run votd")
            print("-" * 30)
            votd = await client.verse_of_the_day()
            print(f"Day: {votd.day}")
            print(f"USFM: {votd.usfm}")
            print()

            print("uv run highlights")
            print("-" * 30)
            highlights = await client.highlights(page=1)
            print(f"Found {len(highlights)} highlights")
            print()

            print("uv run notes")
            print("-" * 30)
            notes = await client.notes(page=1)
            print(f"Found {len(notes)} notes")
            print()

            print("Demo completed. Try from the shell:")
            print("  uv run votd")
            print("  uv run youversion highlights --json")

    except Exception as e:
        print(f"Error: {e}")
        print("Set YOUVERSION_USERNAME and YOUVERSION_PASSWORD in .env")


if __name__ == "__main__":
    asyncio.run(demonstrate_cli_commands())
