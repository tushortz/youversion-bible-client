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
from youversion.enums import MomentKinds, StatusEnum
from youversion.models.moments import CreateMoment, ReferenceCreate


def format_votd(votd) -> str:
    """Format verse of the day for display"""
    # Handle both dict and object
    if isinstance(votd, dict):
        day = votd.get("day", "N/A")
        usfm = votd.get("usfm", [])
        image_id = votd.get("image_id", "None")
    else:
        day = getattr(votd, "day", "N/A")
        usfm = getattr(votd, "usfm", [])
        image_id = getattr(votd, "image_id", "None")

    usfm_str = ", ".join(usfm) if usfm else "N/A"
    return f"""📖 Verse of the Day
Day: {day}
USFM: {usfm_str}
Image ID: {image_id or 'None'}"""


def format_moment(moment, index: int = 1) -> str:
    """Format a moment for display"""
    # Convert Pydantic model to dict if needed
    if hasattr(moment, "model_dump"):
        moment_dict = moment.model_dump()
    else:
        moment_dict = {}

    # Get kind from kind_id if available, otherwise try kind
    kind = moment_dict.get("kind_id") or moment_dict.get("kind")
    if not kind:
        kind = getattr(moment, "kind_id", getattr(moment, "kind", "UNKNOWN"))
    if isinstance(kind, str):
        kind = kind.upper()
    else:
        kind = str(kind).upper()

    # Get title from various possible locations
    title = moment_dict.get("moment_title") or getattr(moment, "moment_title", None)
    if not title:
        # Try to get from base or extras
        base = moment_dict.get("base") or getattr(moment, "base", {})
        extras = moment_dict.get("extras") or getattr(moment, "extras", {})
        if isinstance(base, dict):
            base_title = base.get("title")
            if isinstance(base_title, dict):
                # Title might be a dict with l_args or l_str
                l_args = base_title.get("l_args", {})
                if isinstance(l_args, dict):
                    title = l_args.get("title")
                if not title:
                    title = base_title.get("l_str") or base_title.get("title")
            if not title and isinstance(extras, dict):
                title = extras.get("title")
        elif isinstance(extras, dict):
            title = extras.get("title")
        if not title:
            title = "N/A"

    # Get time_ago if available
    time_ago = moment_dict.get("created_dt") or getattr(moment, "created_dt", "N/A")

    # Get id
    moment_id = moment_dict.get("id") or getattr(moment, "id", "N/A")

    return f"""  {index}. {kind}
     ID: {moment_id}
     Title: {title}
     Time: {time_ago}"""


def format_highlight(highlight, index: int = 1) -> str:
    """Format a highlight for display"""
    # Convert Pydantic model to dict if needed
    if hasattr(highlight, "model_dump"):
        highlight_dict = highlight.model_dump()
    else:
        highlight_dict = {}

    # Get references safely
    references = highlight_dict.get("references") or getattr(highlight, "references", [])
    if not references:
        # Try to get from extras
        extras = highlight_dict.get("extras") or getattr(highlight, "extras", {})
        if isinstance(extras, dict):
            references = extras.get("references", [])

    refs = "N/A"
    if references:
        if isinstance(references[0], dict):
            refs = ", ".join([ref.get("human", "N/A") for ref in references])
        else:
            refs = ", ".join([getattr(ref, "human", "N/A") for ref in references])

    # Get title
    title = highlight_dict.get("moment_title") or getattr(highlight, "moment_title", None)
    if not title:
        base = highlight_dict.get("base") or getattr(highlight, "base", {})
        extras = highlight_dict.get("extras") or getattr(highlight, "extras", {})
        if isinstance(base, dict):
            base_title = base.get("title")
            if isinstance(base_title, dict):
                # Title might be a dict with l_args or l_str
                l_args = base_title.get("l_args", {})
                if isinstance(l_args, dict):
                    title = l_args.get("title")
                if not title:
                    title = base_title.get("l_str") or base_title.get("title")
            if not title and isinstance(extras, dict):
                title = extras.get("title")
        elif isinstance(extras, dict):
            title = extras.get("title")
        if not title:
            title = "N/A"

    time_ago = highlight_dict.get("created_dt") or getattr(highlight, "created_dt", "N/A")

    # Get id
    highlight_id = highlight_dict.get("id") or getattr(highlight, "id", "N/A")

    return f"""  {index}. HIGHLIGHT
     ID: {highlight_id}
     Title: {title}
     References: {refs}
     Time: {time_ago}"""


def format_note(note, index: int = 1) -> str:
    """Format a note for display"""
    # Convert Pydantic model to dict if needed
    if hasattr(note, "model_dump"):
        note_dict = note.model_dump()
    else:
        note_dict = {}

    # Get content safely (no truncation)
    content = note_dict.get("content") or getattr(note, "content", None)
    if not content:
        extras = note_dict.get("extras") or getattr(note, "extras", {})
        if isinstance(extras, dict):
            content = extras.get("content", "N/A")
        else:
            content = "N/A"

    # Get title
    title = note_dict.get("moment_title") or getattr(note, "moment_title", None)
    if not title:
        base = note_dict.get("base") or getattr(note, "base", {})
        extras = note_dict.get("extras") or getattr(note, "extras", {})
        if isinstance(base, dict):
            base_title = base.get("title")
            if isinstance(base_title, dict):
                # Title might be a dict with l_args or l_str
                l_args = base_title.get("l_args", {})
                if isinstance(l_args, dict):
                    title = l_args.get("title")
                if not title:
                    title = base_title.get("l_str") or base_title.get("title")
            if not title and isinstance(extras, dict):
                title = extras.get("title")
        elif isinstance(extras, dict):
            title = extras.get("title")
        if not title:
            title = "N/A"

    # Get status
    status = note_dict.get("status") or getattr(note, "status", None)
    if status:
        if hasattr(status, "value"):
            status_str = status.value
        else:
            status_str = str(status)
    else:
        extras = note_dict.get("extras") or getattr(note, "extras", {})
        if isinstance(extras, dict):
            status_str = extras.get("user_status") or extras.get("system_status", "N/A")
        else:
            status_str = "N/A"

    time_ago = note_dict.get("created_dt") or getattr(note, "created_dt", "N/A")

    # Get id
    note_id = note_dict.get("id") or getattr(note, "id", "N/A")

    return f"""  {index}. NOTE
     ID: {note_id}
     Title: {title}
     Content: {content}
     Status: {status_str}
     Time: {time_ago}"""


def format_generic_item(item: Any, index: int = 1) -> str:
    """Format generic items (bookmarks, images, etc.)"""
    # Handle both dict and object
    if isinstance(item, dict):
        kind = item.get("kind_id") or item.get("kind", "ITEM")
        title = item.get("moment_title") or item.get("title", "N/A")
        time_ago = item.get("created_dt", "N/A")
    else:
        # Pydantic model or object
        kind = getattr(item, "kind_id", getattr(item, "kind", "ITEM"))
        title = getattr(item, "moment_title", None)
        if not title:
            base = getattr(item, "base", {})
            extras = getattr(item, "extras", {})
            if isinstance(base, dict):
                title = base.get("title") or extras.get("title")
            elif isinstance(extras, dict):
                title = extras.get("title")
            if not title:
                title = "N/A"
        time_ago = getattr(item, "created_dt", "N/A")

    if isinstance(kind, str):
        kind = kind.upper()
    else:
        kind = str(kind).upper()

    # Get id
    if isinstance(item, dict):
        item_id = item.get("id", "N/A")
    else:
        item_id = getattr(item, "id", "N/A")

    return f"""  {index}. {kind}
     ID: {item_id}
     Title: {title}
     Time: {time_ago}"""


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

                for i, moment in enumerate(moments, 1):
                    print(format_moment(moment, i))
                    print()

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

                for i, highlight in enumerate(highlights, 1):
                    print(format_highlight(highlight, i))
                    print()

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

                for i, note in enumerate(notes, 1):
                    print(format_note(note, i))
                    print()

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

                for i, bookmark in enumerate(bookmarks, 1):
                    print(format_generic_item(bookmark, i))
                    print()

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

                for i, image in enumerate(images, 1):
                    print(format_generic_item(image, i))
                    if isinstance(image, dict) and "body_image" in image:
                        print(f"     Image: {image['body_image']}")
                    elif hasattr(image, "body_image"):
                        print(f"     Image: {getattr(image, 'body_image', 'N/A')}")
                    print()

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

                for i, item in enumerate(progress, 1):
                    print(format_generic_item(item, i))
                    if isinstance(item, dict) and "percent_complete" in item:
                        print(f"     Progress: {item['percent_complete']}%")
                    elif hasattr(item, "percent_complete"):
                        print(f"     Progress: {getattr(item, 'percent_complete', 'N/A')}%")
                    print()

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

                for i, sub in enumerate(subscriptions, 1):
                    print(format_generic_item(sub, i))
                    if isinstance(sub, dict) and "plan_title" in sub:
                        print(f"     Plan: {sub['plan_title']}")
                    elif hasattr(sub, "plan_title"):
                        print(f"     Plan: {getattr(sub, 'plan_title', 'N/A')}")
                    print()

    except Exception as e:
        print(f"❌ Error getting plan subscriptions: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_plan_completions(args):
    """Get plan completions"""
    try:
        async with AsyncClient() as client:
            completions = await client.plan_completions(page=args.page)

            if args.json:
                print(format_json_output(completions))
            else:
                print(f"✅ Plan Completions (Page {args.page})")
                print(f"Found {len(completions)} completions")
                print("-" * 50)

                for i, completion in enumerate(completions, 1):
                    print(format_generic_item(completion, i))
                    if isinstance(completion, dict) and "plan_title" in completion:
                        print(f"     Plan: {completion['plan_title']}")
                    elif hasattr(completion, "plan_title"):
                        print(f"     Plan: {getattr(completion, 'plan_title', 'N/A')}")
                    print()

    except Exception as e:
        print(f"❌ Error getting plan completions: {e}", file=sys.stderr)
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


async def cmd_create_moment(args):
    """Create a new moment"""
    try:
        # Parse kind enum
        try:
            kind = MomentKinds(args.kind.lower())
        except ValueError:
            valid_kinds = [k.value for k in MomentKinds]
            print(
                f"❌ Error: Invalid kind '{args.kind}'. "
                f"Valid kinds: {', '.join(valid_kinds)}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Parse status enum
        try:
            # StatusEnum values are lowercase: private, draft, public
            status_value = args.status.lower()
            status = StatusEnum(status_value)
        except ValueError:
            valid_statuses = [s.value for s in StatusEnum]
            print(
                f"❌ Error: Invalid status '{args.status}'. "
                f"Valid statuses: {', '.join(valid_statuses)}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Parse references
        references = []
        for ref_str in args.references:
            # Format: "human:version_id:usfm1,usfm2"
            parts = ref_str.split(":")
            if len(parts) < 3:
                print(
                    f"❌ Error: Invalid reference format '{ref_str}'. "
                    "Expected: 'human:version_id:usfm1,usfm2'",
                    file=sys.stderr,
                )
                sys.exit(1)
            human = parts[0]
            try:
                version_id = int(parts[1])
            except ValueError:
                print(
                    f"❌ Error: Invalid version_id '{parts[1]}' in "
                    f"reference '{ref_str}'. Must be an integer.",
                    file=sys.stderr,
                )
                sys.exit(1)
            usfm = parts[2].split(",")
            references.append(
                ReferenceCreate(human=human, version_id=version_id, usfm=usfm)
            )

        # Parse labels
        labels = [label.strip() for label in args.labels.split(",") if label.strip()]

        # Create moment model
        moment = CreateMoment(
            kind=kind,
            content=args.content,
            references=references,
            title=args.title,
            status=status,
            body=args.body,
            color=args.color,
            labels=labels,
            language_tag=args.language_tag,
        )

        async with AsyncClient() as client:
            result = await client.create_moment(moment)

            if args.json:
                print(format_json_output(result))
            else:
                print("✅ Moment created successfully!")
                print("-" * 50)
                if "errors" in result:
                    print("⚠️  Warnings/Errors:")
                    for error in result["errors"]:
                        print(f"  - {error}")
                else:
                    print(f"Kind: {moment.kind.value}")
                    print(f"Title: {moment.title}")
                    print(f"Status: {moment.status.value}")
                    print(f"References: {len(moment.references)}")

    except ValueError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating moment: {e}", file=sys.stderr)
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
  youversion plan-completions        # Get plan completions
  youversion convert-notes           # Convert notes to markdown
  youversion create-moment --kind note --content "My note" --title "Title" --status private --body "Body" --color ff0000 --language-tag en --references "Genesis 1:1:1:GEN.1.1" --labels "test"

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

    # Plan completions
    completions_parser = subparsers.add_parser(
        "plan-completions", help="Get plan completions"
    )
    completions_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Convert notes
    convert_parser = subparsers.add_parser(
        "convert-notes", help="Convert notes to markdown"
    )

    # Create moment
    create_moment_parser = subparsers.add_parser(
        "create-moment", help="Create a new moment"
    )
    create_moment_parser.add_argument(
        "--kind",
        type=str,
        required=True,
        help="Type of moment (note, highlight, bookmark, image, badge)",
    )
    create_moment_parser.add_argument(
        "--content", type=str, required=True, help="Content text"
    )
    create_moment_parser.add_argument(
        "--title", type=str, required=True, help="Moment title"
    )
    create_moment_parser.add_argument(
        "--status",
        type=str,
        required=True,
        help="Status (private, draft, or public)",
    )
    create_moment_parser.add_argument(
        "--body", type=str, required=True, help="Body text"
    )
    create_moment_parser.add_argument(
        "--color",
        type=str,
        required=True,
        help="Color hex code (6 characters, e.g., ff0000)",
    )
    create_moment_parser.add_argument(
        "--language-tag",
        type=str,
        required=True,
        dest="language_tag",
        help="Language tag (2 characters, e.g., en)",
    )
    create_moment_parser.add_argument(
        "--references",
        type=str,
        nargs="+",
        required=True,
        help="Bible references in format 'human:version_id:usfm1,usfm2' "
        "(can specify multiple)",
    )
    create_moment_parser.add_argument(
        "--labels",
        type=str,
        required=True,
        help="Comma-separated list of labels (1-10 labels)",
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
                "plan-completions": completions_parser,
                "convert-notes": convert_parser,
                "create-moment": create_moment_parser,
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
        "plan-completions": cmd_plan_completions,
        "convert-notes": cmd_convert_notes,
        "create-moment": cmd_create_moment,
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


def poetry_cmd_plan_completions():
    """Poetry script entry point for plan-completions command"""
    parser = create_parser()
    args = parser.parse_args(["plan-completions"])
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_plan_completions(args)
    asyncio.run(cmd_plan_completions(args))


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


def poetry_cmd_create_moment():
    """Poetry script entry point for create-moment command"""
    parser = create_parser()
    args = parser.parse_args()
    check_credentials()
    try:
        is_running = asyncio.get_event_loop().is_running()
    except RuntimeError:
        is_running = False
    if is_running:
        return cmd_create_moment(args)
    asyncio.run(cmd_create_moment(args))


async def cmd_discover_endpoints(args):
    """Discover available API endpoints"""
    try:
        # URLDiscovery imported at module level for easier test patching

        print("🔍 Discovering YouVersion API endpoints...")
        print("=" * 50)

        # Get username from args or environment variables
        username = getattr(args, "username", None)
        if not username:
            load_dotenv()
            username = os.getenv("YOUVERSION_USERNAME")
            if not username:
                # Try to get from authenticated client as fallback
                try:
                    async with AsyncClient() as client:
                        username = client.username
                except Exception:
                    print(
                        "❌ Error: Username not provided. "
                        "Please provide --username or set YOUVERSION_USERNAME",
                        file=sys.stderr,
                    )
                    sys.exit(1)

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
        print(f"❌ Error discovering endpoints: {e}", file=sys.stderr)
        sys.exit(1)


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
