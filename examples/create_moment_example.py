#!/usr/bin/env python3
"""
Example demonstrating how to create moments (notes, highlights, etc.)

This example shows how to use the CreateMoment model to create new moments
with proper validation and error handling.
"""

import asyncio
import os

from youversion.clients import AsyncClient
from youversion.enums import MomentKinds, StatusEnum
from youversion.models.moments import CreateMoment, ReferenceCreate


async def create_note_example(client: AsyncClient):
    """Example: Create a note moment"""
    print("\n📝 Creating a Note Moment")
    print("-" * 50)

    try:
        # Create a reference
        reference = ReferenceCreate(human="John 3:16", version_id=1, usfm=["JHN.3.16"])

        # Create the moment
        moment = CreateMoment(
            kind=MomentKinds.NOTE,
            content="This is a test note about John 3:16",
            references=[reference],
            title="My Test Note",
            status=StatusEnum.PRIVATE,
            body="This is the body of my note. It can contain more detailed information.",
            color="ff0000",  # Red color
            labels=["test", "favorite"],
            language_tag="en",
        )

        # Create the moment via API
        result = await client.create_moment(moment)

        print("✅ Note created successfully!")
        if isinstance(result, dict):
            if "errors" in result:
                print("⚠️  Warnings/Errors:")
                for error in result["errors"]:
                    print(f"  - {error}")
            else:
                print(f"  Moment ID: {result.get('id', 'N/A')}")
        else:
            print(f"  Result: {result}")

    except Exception as e:
        print(f"❌ Error creating note: {e}")


async def create_highlight_example(client: AsyncClient):
    """Example: Create a highlight moment"""
    print("\n✨ Creating a Highlight Moment")
    print("-" * 50)

    try:
        # Create multiple references
        references = [
            ReferenceCreate(human="Genesis 1:1", version_id=1, usfm=["GEN.1.1"]),
            ReferenceCreate(human="John 1:1", version_id=1, usfm=["JHN.1.1"]),
        ]

        # Create the highlight
        moment = CreateMoment(
            kind=MomentKinds.HIGHLIGHT,
            content="In the beginning",
            references=references,
            title="Creation Highlights",
            status=StatusEnum.PRIVATE,
            body="Highlighting verses about creation",
            color="ffff00",  # Yellow color
            labels=["creation", "beginning"],
            language_tag="en",
        )

        # Create the moment via API
        result = await client.create_moment(moment)

        print("✅ Highlight created successfully!")
        if isinstance(result, dict):
            if "errors" in result:
                print("⚠️  Warnings/Errors:")
                for error in result["errors"]:
                    print(f"  - {error}")
            else:
                print(f"  Moment ID: {result.get('id', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creating highlight: {e}")


async def create_moment_from_dict_example(client: AsyncClient):
    """Example: Create a moment using a dictionary"""
    print("\n📋 Creating a Moment from Dictionary")
    print("-" * 50)

    try:
        # Create moment data as dictionary
        moment_dict = {
            "kind": "note",
            "content": "This note was created from a dictionary",
            "references": [
                {"human": "Psalm 23:1", "version_id": 1, "usfm": ["PSA.23.1"]}
            ],
            "title": "Dictionary Note",
            "status": "private",
            "body": "This demonstrates creating a moment from a dict",
            "color": "00ff00",  # Green color
            "labels": ["dict", "example"],
            "language_tag": "en",
        }

        # Create the moment via API (client will convert dict to CreateMoment)
        result = await client.create_moment(moment_dict)

        print("✅ Moment created successfully from dictionary!")
        if isinstance(result, dict):
            if "errors" in result:
                print("⚠️  Warnings/Errors:")
                for error in result["errors"]:
                    print(f"  - {error}")
            else:
                print(f"  Moment ID: {result.get('id', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creating moment from dict: {e}")


async def get_moment_details_example(client: AsyncClient, moment_id: int):
    """Example: Get moment details"""
    print(f"\n🔍 Getting Moment Details (ID: {moment_id})")
    print("-" * 50)

    try:
        moment = await client.get_moment_details(moment_id)
        print("✅ Moment details retrieved!")
        if isinstance(moment, dict):
            print(f"  ID: {moment.get('id', 'N/A')}")
            print(f"  Kind: {moment.get('kind_id', 'N/A')}")
            print(f"  Title: {moment.get('moment_title', 'N/A')}")
        else:
            moment_dict = moment.model_dump() if hasattr(moment, "model_dump") else {}
            print(f"  ID: {moment_dict.get('id', 'N/A')}")
            print(f"  Kind: {moment_dict.get('kind_id', 'N/A')}")

    except Exception as e:
        print(f"❌ Error getting moment details: {e}")


async def list_user_moments_example(client: AsyncClient):
    """Example: List user's moments with filters"""
    print("\n📋 Listing User Moments")
    print("-" * 50)

    try:
        # Get all moments
        all_moments = await client.get_moments(page=1)
        print(
            f"✅ Found {len(all_moments) if isinstance(all_moments, list) else 'N/A'} total moments"
        )

        # Get only notes
        notes = await client.get_moments(page=1, kind="note")
        print(f"✅ Found {len(notes) if isinstance(notes, list) else 'N/A'} notes")

        # Get moments for specific verse
        verse_moments = await client.get_moments(page=1, usfm="JHN.3.16")
        print(
            f"✅ Found {len(verse_moments) if isinstance(verse_moments, list) else 'N/A'} moments for JHN.3.16"
        )

    except Exception as e:
        print(f"❌ Error listing moments: {e}")


async def main():
    """Main function demonstrating moment creation"""
    print("🎯 YouVersion Bible Client - Create Moment Examples")
    print("=" * 80)

    # Check if credentials are available
    username = os.getenv("YOUVERSION_USERNAME")
    password = os.getenv("YOUVERSION_PASSWORD")

    if not username or not password:
        print(
            "❌ Error: Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables"
        )
        print("   Or create a .env file with your credentials")
        return

    try:
        async with AsyncClient() as client:
            print(f"✅ Connected as: {client.username}")
            print(f"✅ User ID: {client.user_id}")

            # Demonstrate moment creation
            await create_note_example(client)
            await create_highlight_example(client)
            await create_moment_from_dict_example(client)

            # Demonstrate getting moment details (using a placeholder ID)
            # In practice, you'd use the ID returned from create_moment
            # await get_moment_details_example(client, 12345)

            # Demonstrate listing moments
            await list_user_moments_example(client)

            print("\n✅ Create moment examples completed!")
            print("\n💡 Tips:")
            print("   - Use CreateMoment model for type safety and validation")
            print("   - Use dictionaries for quick prototyping")
            print("   - All enum values are validated automatically")
            print("   - References must include human, version_id, and usfm")
            print("   - Labels must be 1-10 items")
            print("   - Color must be 6-character hex code")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
