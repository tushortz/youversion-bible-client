#!/usr/bin/env python3
"""
Command Line Interface for YouVersion Bible Client

This CLI provides access to all public methods of the YouVersion Bible Client.
Supports async operations and provides formatted output for all data types.

Usage:
    youversion --help
    youversion votd [--day DAY]
    youversion moments [--page PAGE]
    youversion highlights [--page PAGE]
    youversion notes [--page PAGE]
    youversion bookmarks [--page PAGE]
    youversion images [--page PAGE]
    youversion plan-progress [--page PAGE]
    youversion plan-subscriptions [--page PAGE]
    youversion convert-notes
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv

from youversion.clients import AsyncClient
from youversion.core.url_discovery import URLDiscovery


def format_votd(votd) -> str:
    """Format verse of the day for display"""
    return f"""📖 Verse of the Day
Day: {votd.day}
USFM: {', '.join(votd.usfm)}
Image ID: {votd.image_id or 'None'}"""


def format_moment(moment, index: int = 1) -> str:
    """Format a moment for display"""
    return f"""  {index}. {moment.kind.upper()}
     Title: {moment.moment_title}
     Time: {moment.time_ago}
     Owned by me: {moment.owned_by_me}"""


def format_highlight(highlight, index: int = 1) -> str:
    """Format a highlight for display"""
    refs = ", ".join([ref.human for ref in highlight.references[:3]])
    if len(highlight.references) > 3:
        refs += f" (+{len(highlight.references) - 3} more)"

    return f"""  {index}. HIGHLIGHT
     Title: {highlight.moment_title}
     References: {refs}
     Time: {highlight.time_ago}"""


def format_note(note, index: int = 1) -> str:
    """Format a note for display"""
    content = note.content[:100] + "..." if len(note.content) > 100 else note.content

    return f"""  {index}. NOTE
     Title: {note.moment_title}
     Content: {content}
     Status: {note.status.value}
     Time: {note.time_ago}"""


def format_generic_item(item: dict[str, Any], index: int = 1) -> str:
    """Format generic items (bookmarks, images, etc.)"""
    return f"""  {index}. {item.get('kind', 'ITEM').upper()}
     Title: {item.get('moment_title', 'N/A')}
     Time: {item.get('time_ago', 'N/A')}"""


def format_json_output(data: Any) -> str:
    """Format data as JSON"""
    if hasattr(data, "dict"):
        return json.dumps(data.model_dump(), indent=2, default=str)
    elif isinstance(data, list):
        return json.dumps(
            [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in data
            ],
            indent=2,
            default=str,
        )
    else:
        return json.dumps(data, indent=2, default=str)


async def cmd_votd(args):
    """Get verse of the day"""
    try:
        async with AsyncClient() as client:
            votd = await client.verse_of_the_day(day=args.day)

            if args.json:
                print(format_json_output(votd))
            else:
                print(format_votd(votd))

    except Exception as e:
        print(f"❌ Error getting verse of the day: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_moments(args):
    """Get moments"""
    try:
        async with AsyncClient() as client:
            moments = await client.moments(page=args.page)

            if args.json:
                print(format_json_output(moments))
            else:
                print(f"📋 Moments (Page {args.page})")
                print(f"Found {len(moments)} moments")
                print("-" * 50)

                for i, moment in enumerate(moments[: args.limit], 1):
                    print(format_moment(moment, i))

                if len(moments) > args.limit:
                    print(f"\n... and {len(moments) - args.limit} more moments")

    except Exception as e:
        print(f"❌ Error getting moments: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_highlights(args):
    """Get highlights"""
    try:
        async with AsyncClient() as client:
            highlights = await client.highlights(page=args.page)

            if args.json:
                print(format_json_output(highlights))
            else:
                print(f"✨ Highlights (Page {args.page})")
                print(f"Found {len(highlights)} highlights")
                print("-" * 50)

                for i, highlight in enumerate(highlights[: args.limit], 1):
                    print(format_highlight(highlight, i))

                if len(highlights) > args.limit:
                    print(f"\n... and {len(highlights) - args.limit} more highlights")

    except Exception as e:
        print(f"❌ Error getting highlights: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_notes(args):
    """Get notes"""
    try:
        async with AsyncClient() as client:
            notes = await client.notes(page=args.page)

            if args.json:
                print(format_json_output(notes))
            else:
                print(f"📝 Notes (Page {args.page})")
                print(f"Found {len(notes)} notes")
                print("-" * 50)

                for i, note in enumerate(notes[: args.limit], 1):
                    print(format_note(note, i))

                if len(notes) > args.limit:
                    print(f"\n... and {len(notes) - args.limit} more notes")

    except Exception as e:
        print(f"❌ Error getting notes: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_bookmarks(args):
    """Get bookmarks"""
    try:
        async with AsyncClient() as client:
            bookmarks = await client.bookmarks(page=args.page)

            if args.json:
                print(format_json_output(bookmarks))
            else:
                print(f"🔖 Bookmarks (Page {args.page})")
                print(f"Found {len(bookmarks)} bookmarks")
                print("-" * 50)

                for i, bookmark in enumerate(bookmarks[: args.limit], 1):
                    print(format_generic_item(bookmark, i))

                if len(bookmarks) > args.limit:
                    print(f"\n... and {len(bookmarks) - args.limit} more bookmarks")

    except Exception as e:
        print(f"❌ Error getting bookmarks: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_images(args):
    """Get images"""
    try:
        async with AsyncClient() as client:
            images = await client.my_images(page=args.page)

            if args.json:
                print(format_json_output(images))
            else:
                print(f"🖼️  Images (Page {args.page})")
                print(f"Found {len(images)} images")
                print("-" * 50)

                for i, image in enumerate(images[: args.limit], 1):
                    print(format_generic_item(image, i))
                    if "body_image" in image:
                        print(f"     Image: {image['body_image'][:50]}...")

                if len(images) > args.limit:
                    print(f"\n... and {len(images) - args.limit} more images")

    except Exception as e:
        print(f"❌ Error getting images: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_plan_progress(args):
    """Get plan progress"""
    try:
        async with AsyncClient() as client:
            progress = await client.plan_progress(page=args.page)

            if args.json:
                print(format_json_output(progress))
            else:
                print(f"📊 Plan Progress (Page {args.page})")
                print(f"Found {len(progress)} progress items")
                print("-" * 50)

                for i, item in enumerate(progress[: args.limit], 1):
                    print(format_generic_item(item, i))
                    if "percent_complete" in item:
                        print(f"     Progress: {item['percent_complete']}%")

                if len(progress) > args.limit:
                    print(f"\n... and {len(progress) - args.limit} more items")

    except Exception as e:
        print(f"❌ Error getting plan progress: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_plan_subscriptions(args):
    """Get plan subscriptions"""
    try:
        async with AsyncClient() as client:
            subscriptions = await client.plan_subscriptions(page=args.page)

            if args.json:
                print(format_json_output(subscriptions))
            else:
                print(f"📅 Plan Subscriptions (Page {args.page})")
                print(f"Found {len(subscriptions)} subscriptions")
                print("-" * 50)

                for i, sub in enumerate(subscriptions[: args.limit], 1):
                    print(format_generic_item(sub, i))
                    if "plan_title" in sub:
                        print(f"     Plan: {sub['plan_title']}")

                if len(subscriptions) > args.limit:
                    print(
                        f"\n... and {len(subscriptions) - args.limit} more subscriptions"
                    )

    except Exception as e:
        print(f"❌ Error getting plan subscriptions: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_convert_notes(args):
    """Convert notes to markdown"""
    try:
        async with AsyncClient() as client:
            notes_md = await client.convert_note_to_md()

            if args.json:
                print(format_json_output(notes_md))
            else:
                print("📄 Converted Notes to Markdown")
                print(f"Processed {len(notes_md)} notes")
                print("-" * 50)

                if notes_md:
                    print("Note data structure:")
                    print(f"  Type: {type(notes_md)}")
                    print(f"  Length: {len(notes_md)}")
                    if notes_md and isinstance(notes_md[0], dict):
                        print(f"  First note keys: {list(notes_md[0].keys())}")

    except Exception as e:
        print(f"❌ Error converting notes: {e}", file=sys.stderr)
        sys.exit(1)


def check_credentials():
    """Check if credentials are available"""
    load_dotenv()

    username = os.getenv("YOUVERSION_USERNAME")
    password = os.getenv("YOUVERSION_PASSWORD")

    if not username or not password:
        print("❌ Error: Missing credentials", file=sys.stderr)
        print(
            "Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables",
            file=sys.stderr,
        )
        print("Or create a .env file with your credentials:", file=sys.stderr)
        print("", file=sys.stderr)
        print("YOUVERSION_USERNAME=your_username", file=sys.stderr)
        print("YOUVERSION_PASSWORD=your_password", file=sys.stderr)
        sys.exit(1)


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="YouVersion Bible Client CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  youversion votd                    # Get current day's verse
  youversion votd --day 100          # Get verse for day 100
  youversion moments --page 2       # Get moments from page 2
  youversion highlights --limit 5   # Show only 5 highlights
  youversion notes --json            # Output as JSON
  youversion bookmarks --page 1      # Get bookmarks from page 1
  youversion images --page 1         # Get images from page 1
  youversion plan-progress           # Get plan progress
  youversion plan-subscriptions      # Get plan subscriptions
  youversion convert-notes           # Convert notes to markdown

Environment Variables:
  YOUVERSION_USERNAME    Your YouVersion username
  YOUVERSION_PASSWORD    Your YouVersion password

Or create a .env file in the project root with these variables.
        """,
    )

    # Global options
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Limit number of items to display (default: 10)",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Verse of the day
    votd_parser = subparsers.add_parser("votd", help="Get verse of the day")
    votd_parser.add_argument("--day", type=int, help="Specific day number (1-365)")

    # Moments
    moments_parser = subparsers.add_parser("moments", help="Get moments")
    moments_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Highlights
    highlights_parser = subparsers.add_parser("highlights", help="Get highlights")
    highlights_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Notes
    notes_parser = subparsers.add_parser("notes", help="Get notes")
    notes_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Bookmarks
    bookmarks_parser = subparsers.add_parser("bookmarks", help="Get bookmarks")
    bookmarks_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Images
    images_parser = subparsers.add_parser("images", help="Get images")
    images_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Plan progress
    progress_parser = subparsers.add_parser("plan-progress", help="Get plan progress")
    progress_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Plan subscriptions
    subscriptions_parser = subparsers.add_parser(
        "plan-subscriptions", help="Get plan subscriptions"
    )
    subscriptions_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Convert notes
    convert_parser = subparsers.add_parser(
        "convert-notes", help="Convert notes to markdown"
    )

    # Discover endpoints
    discover_parser = subparsers.add_parser(
        "discover-endpoints", help="Discover available API endpoints and build ID"
    )
    discover_parser.add_argument(
        "--username", type=str, help="Username to test endpoints for"
    )

    # Ensure choices mapping is populated for tests that inspect it directly
    try:
        action = parser._subparsers._actions[0]
        action.choices = action.choices or {}
        action.choices.update(
            {
                "votd": votd_parser,
                "moments": moments_parser,
                "highlights": highlights_parser,
                "notes": notes_parser,
                "bookmarks": bookmarks_parser,
                "images": images_parser,
                "plan-progress": progress_parser,
                "plan-subscriptions": subscriptions_parser,
                "convert-notes": convert_parser,
                "discover-endpoints": discover_parser,
            }
        )
    except Exception:
        pass

    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check credentials
    check_credentials()

    # Command mapping
    commands = {
        "votd": cmd_votd,
        "moments": cmd_moments,
        "highlights": cmd_highlights,
        "notes": cmd_notes,
        "bookmarks": cmd_bookmarks,
        "images": cmd_images,
        "plan-progress": cmd_plan_progress,
        "plan-subscriptions": cmd_plan_subscriptions,
        "convert-notes": cmd_convert_notes,
        "discover-endpoints": cmd_discover_endpoints,
    }

    # Execute command
    command_func = commands[args.command]
    # Avoid nested asyncio.run during tests/async contexts
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        # In async context, schedule the coroutine
        return command_func(args)
    asyncio.run(command_func(args))


# Poetry script entry points
def poetry_cmd_votd():
    """Poetry script entry point for votd command"""
    parser = create_parser()
    args = parser.parse_args(["votd"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_votd(args)
    asyncio.run(cmd_votd(args))


def poetry_cmd_moments():
    """Poetry script entry point for moments command"""
    parser = create_parser()
    args = parser.parse_args(["moments"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_moments(args)
    asyncio.run(cmd_moments(args))


def poetry_cmd_highlights():
    """Poetry script entry point for highlights command"""
    parser = create_parser()
    args = parser.parse_args(["highlights"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_highlights(args)
    asyncio.run(cmd_highlights(args))


def poetry_cmd_notes():
    """Poetry script entry point for notes command"""
    parser = create_parser()
    args = parser.parse_args(["notes"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_notes(args)
    asyncio.run(cmd_notes(args))


def poetry_cmd_bookmarks():
    """Poetry script entry point for bookmarks command"""
    parser = create_parser()
    args = parser.parse_args(["bookmarks"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_bookmarks(args)
    asyncio.run(cmd_bookmarks(args))


def poetry_cmd_images():
    """Poetry script entry point for images command"""
    parser = create_parser()
    args = parser.parse_args(["images"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_images(args)
    asyncio.run(cmd_images(args))


def poetry_cmd_plan_progress():
    """Poetry script entry point for plan-progress command"""
    parser = create_parser()
    args = parser.parse_args(["plan-progress"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_plan_progress(args)
    asyncio.run(cmd_plan_progress(args))


def poetry_cmd_plan_subscriptions():
    """Poetry script entry point for plan-subscriptions command"""
    parser = create_parser()
    args = parser.parse_args(["plan-subscriptions"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_plan_subscriptions(args)
    asyncio.run(cmd_plan_subscriptions(args))


def poetry_cmd_convert_notes():
    """Poetry script entry point for convert-notes command"""
    parser = create_parser()
    args = parser.parse_args(["convert-notes"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_convert_notes(args)
    asyncio.run(cmd_convert_notes(args))


async def cmd_discover_endpoints(args):
    """Discover available API endpoints"""
    try:
        # URLDiscovery imported at module level for easier test patching

        print("🔍 Discovering YouVersion API endpoints...")
        print("=" * 50)

        # Get username from args or active client when available
        username = getattr(args, "username", None)
        if not username:
            async with AsyncClient() as client:
                username = client.username

        print(f"📋 Testing endpoints for user: {username}")
        print()

        # Discover endpoints
        endpoints = await URLDiscovery.discover_endpoints(username)

        print("📡 Available endpoints:")
        for name, url in endpoints.items():
            print(f"  {name}: {url}")
        print()

        # Test endpoints individually using URLDiscovery.test_endpoint
        print("🧪 Testing endpoint accessibility...")
        for name, url in endpoints.items():
            result = await URLDiscovery.test_endpoint(url)
            if not result:
                # Skip if no result (e.g., mocked test returns None)
                continue
            status = "✅" if result.get("accessible") else "❌"
            status_code = result.get("status_code") or "ERROR"
            print(f"  {status} {name}: {status_code}")
            if result.get("redirects") and result.get("redirect_url"):
                print(f"    ↳ Redirects to: {result['redirect_url']}")
            if result.get("requires_auth"):
                print("    🔐 Requires authentication")

        print()

    except Exception as e:
        print(f"❌ Error discovering endpoints: {e}")


def poetry_cmd_discover_endpoints():
    """Poetry script entry point for discover-endpoints command"""
    parser = create_parser()
    args = parser.parse_args(["discover-endpoints"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_discover_endpoints(args)
    asyncio.run(cmd_discover_endpoints(args))


if __name__ == "__main__":
    main()
