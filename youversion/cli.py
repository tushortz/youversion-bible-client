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
    youversion badges [--page PAGE]
    youversion plan-progress [--page PAGE]
    youversion plan-subscriptions [--page PAGE]
    youversion plan-completions [--page PAGE]
    youversion convert-notes
    youversion create-moment [options]
    youversion search-bible QUERY [options]
    youversion get-bible-chapter REFERENCE [options]
    youversion get-themes [options]
    ... and many more commands
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv

from youversion.clients import AsyncClient
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
    references = highlight_dict.get("references") or getattr(
        highlight, "references", []
    )
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
    title = highlight_dict.get("moment_title") or getattr(
        highlight, "moment_title", None
    )
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

    time_ago = highlight_dict.get("created_dt") or getattr(
        highlight, "created_dt", "N/A"
    )

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
                        print(
                            f"     Progress: {getattr(item, 'percent_complete', 'N/A')}%"
                        )
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


async def cmd_badges(args):
    """Get badges"""
    try:
        async with AsyncClient() as client:
            badges = await client.badges(page=args.page)

            if args.json:
                print(format_json_output(badges))
            else:
                print(f"🏅 Badges (Page {args.page})")
                print(f"Found {len(badges)} badges")
                print("-" * 50)

                for i, badge in enumerate(badges, 1):
                    print(format_generic_item(badge, i))
                    print()

    except Exception as e:
        print(f"❌ Error getting badges: {e}", file=sys.stderr)
        sys.exit(1)


# Bible API commands
async def cmd_get_bible_configuration(args):
    """Get Bible configuration"""
    try:
        async with AsyncClient() as client:
            config = await client.get_bible_configuration()
            print(format_json_output(config) if args.json else str(config))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_bible_versions(args):
    """Get Bible versions"""
    try:
        async with AsyncClient() as client:
            versions = await client.get_bible_versions(
                language_tag=args.language_tag, version_type=args.version_type
            )
            print(format_json_output(versions) if args.json else str(versions))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_bible_version(args):
    """Get specific Bible version"""
    try:
        async with AsyncClient() as client:
            version = await client.get_bible_version(args.version_id)
            print(format_json_output(version) if args.json else str(version))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_bible_chapter(args):
    """Get Bible chapter"""
    try:
        async with AsyncClient() as client:
            chapter = await client.get_bible_chapter(
                reference=args.reference, version_id=args.version_id
            )
            print(format_json_output(chapter) if args.json else str(chapter))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_recommended_languages(args):
    """Get recommended languages"""
    try:
        async with AsyncClient() as client:
            languages = await client.get_recommended_languages(args.country)
            print(format_json_output(languages) if args.json else str(languages))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Audio API commands
async def cmd_get_audio_chapter(args):
    """Get audio chapter"""
    try:
        async with AsyncClient() as client:
            chapter = await client.get_audio_chapter(
                reference=args.reference, version_id=args.version_id
            )
            print(format_json_output(chapter) if args.json else str(chapter))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_audio_version(args):
    """Get audio version"""
    try:
        async with AsyncClient() as client:
            version = await client.get_audio_version(args.audio_id)
            print(format_json_output(version) if args.json else str(version))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Search API commands
async def cmd_search_bible(args):
    """Search Bible text"""
    try:
        async with AsyncClient() as client:
            results = await client.search_bible(
                query=args.query,
                version_id=args.version_id,
                book=args.book,
                page=args.page,
            )
            print(format_json_output(results) if args.json else str(results))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_search_plans(args):
    """Search reading plans"""
    try:
        async with AsyncClient() as client:
            results = await client.search_plans(
                query=args.query, language_tag=args.language_tag, page=args.page
            )
            print(format_json_output(results) if args.json else str(results))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_search_users(args):
    """Search users"""
    try:
        async with AsyncClient() as client:
            results = await client.search_users(
                query=args.query, language_tag=args.language_tag, page=args.page
            )
            print(format_json_output(results) if args.json else str(results))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Video API commands
async def cmd_get_videos(args):
    """Get videos"""
    try:
        async with AsyncClient() as client:
            videos = await client.get_videos(args.language_tag)
            print(format_json_output(videos) if args.json else str(videos))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_video_details(args):
    """Get video details"""
    try:
        async with AsyncClient() as client:
            video = await client.get_video_details(args.video_id)
            print(format_json_output(video) if args.json else str(video))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Image API commands (different from my_images)
async def cmd_get_images(args):
    """Get images for a reference"""
    try:
        async with AsyncClient() as client:
            images = await client.get_images(
                reference=args.reference, language_tag=args.language_tag, page=args.page
            )
            print(format_json_output(images) if args.json else str(images))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_image_upload_url(args):
    """Get image upload URL"""
    try:
        async with AsyncClient() as client:
            url_data = await client.get_image_upload_url()
            print(format_json_output(url_data) if args.json else str(url_data))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Event API commands
async def cmd_search_events(args):
    """Search events"""
    try:
        async with AsyncClient() as client:
            results = await client.search_events(
                query=args.query,
                latitude=args.latitude,
                longitude=args.longitude,
                page=args.page,
            )
            print(format_json_output(results) if args.json else str(results))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_event_details(args):
    """Get event details"""
    try:
        async with AsyncClient() as client:
            event = await client.get_event_details(args.event_id)
            print(format_json_output(event) if args.json else str(event))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_saved_events(args):
    """Get saved events"""
    try:
        async with AsyncClient() as client:
            events = await client.get_saved_events(args.page)
            print(format_json_output(events) if args.json else str(events))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_save_event(args):
    """Save event"""
    try:
        comments = None
        if args.comments:
            comments = json.loads(args.comments)
        async with AsyncClient() as client:
            result = await client.save_event(args.event_id, comments)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_delete_saved_event(args):
    """Delete saved event"""
    try:
        async with AsyncClient() as client:
            result = await client.delete_saved_event(args.event_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_all_saved_event_ids(args):
    """Get all saved event IDs"""
    try:
        async with AsyncClient() as client:
            ids = await client.get_all_saved_event_ids()
            print(format_json_output(ids) if args.json else str(ids))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_event_configuration(args):
    """Get event configuration"""
    try:
        async with AsyncClient() as client:
            config = await client.get_event_configuration()
            print(format_json_output(config) if args.json else str(config))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Moment management commands
async def cmd_get_moments(args):
    """Get moments list"""
    try:
        async with AsyncClient() as client:
            moments = await client.get_moments(
                page=args.page,
                user_id=args.user_id,
                kind=args.kind,
                version_id=args.version_id,
                usfm=args.usfm,
            )
            print(format_json_output(moments) if args.json else str(moments))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_moment_details(args):
    """Get moment details"""
    try:
        async with AsyncClient() as client:
            moment = await client.get_moment_details(args.moment_id)
            print(format_json_output(moment) if args.json else str(moment))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_update_moment(args):
    """Update moment"""
    try:
        data = json.loads(args.data)
        async with AsyncClient() as client:
            result = await client.update_moment(data)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_delete_moment(args):
    """Delete moment"""
    try:
        async with AsyncClient() as client:
            result = await client.delete_moment(args.moment_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_moment_colors(args):
    """Get moment colors"""
    try:
        async with AsyncClient() as client:
            colors = await client.get_moment_colors()
            print(format_json_output(colors) if args.json else str(colors))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_moment_labels(args):
    """Get moment labels"""
    try:
        async with AsyncClient() as client:
            labels = await client.get_moment_labels()
            print(format_json_output(labels) if args.json else str(labels))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_verse_colors(args):
    """Get verse colors"""
    try:
        async with AsyncClient() as client:
            colors = await client.get_verse_colors(
                usfm=args.usfm, version_id=args.version_id
            )
            print(format_json_output(colors) if args.json else str(colors))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_hide_verse_colors(args):
    """Hide verse colors"""
    try:
        data = json.loads(args.data)
        async with AsyncClient() as client:
            result = await client.hide_verse_colors(data)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_moments_configuration(args):
    """Get moments configuration"""
    try:
        async with AsyncClient() as client:
            config = await client.get_moments_configuration()
            print(format_json_output(config) if args.json else str(config))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Comment commands
async def cmd_create_comment(args):
    """Create comment"""
    try:
        async with AsyncClient() as client:
            result = await client.create_comment(
                moment_id=args.moment_id, comment=args.comment
            )
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_delete_comment(args):
    """Delete comment"""
    try:
        async with AsyncClient() as client:
            result = await client.delete_comment(args.comment_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Like commands
async def cmd_like_moment(args):
    """Like moment"""
    try:
        async with AsyncClient() as client:
            result = await client.like_moment(args.moment_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_unlike_moment(args):
    """Unlike moment"""
    try:
        async with AsyncClient() as client:
            result = await client.unlike_moment(args.moment_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Device commands
async def cmd_register_device(args):
    """Register device"""
    try:
        async with AsyncClient() as client:
            result = await client.register_device(
                device_id=args.device_id,
                device_type=args.device_type,
                user_id=args.user_id,
                old_device_id=args.old_device_id,
                tags=args.tags,
            )
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_unregister_device(args):
    """Unregister device"""
    try:
        async with AsyncClient() as client:
            result = await client.unregister_device(args.device_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Theme commands
async def cmd_get_themes(args):
    """Get themes"""
    try:
        async with AsyncClient() as client:
            themes = await client.get_themes(
                page=args.page, language_tag=args.language_tag
            )
            print(format_json_output(themes) if args.json else str(themes))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_add_theme(args):
    """Add theme"""
    try:
        available_locales = args.available_locales.split(",")
        colors = json.loads(args.colors)
        cta_urls = json.loads(args.cta_urls)
        version_ids = json.loads(args.version_ids)
        async with AsyncClient() as client:
            result = await client.add_theme(
                theme_id=args.theme_id,
                available_locales=available_locales,
                colors=colors,
                cta_urls=cta_urls,
                msgid_suffix=args.msgid_suffix,
                version_ids=version_ids,
            )
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_remove_theme(args):
    """Remove theme"""
    try:
        async with AsyncClient() as client:
            result = await client.remove_theme(args.theme_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_set_theme(args):
    """Set theme"""
    try:
        async with AsyncClient() as client:
            result = await client.set_theme(
                theme_id=args.theme_id, previous_theme_id=args.previous_theme_id
            )
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_get_theme_description(args):
    """Get theme description"""
    try:
        async with AsyncClient() as client:
            description = await client.get_theme_description(
                theme_id=args.theme_id, language_tag=args.language_tag
            )
            print(format_json_output(description) if args.json else str(description))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Friend commands
async def cmd_send_friend_request(args):
    """Send friend request"""
    try:
        async with AsyncClient() as client:
            result = await client.send_friend_request(args.user_id)
            print(format_json_output(result) if args.json else str(result))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Localization commands
async def cmd_get_localization_items(args):
    """Get localization items"""
    try:
        async with AsyncClient() as client:
            items = await client.get_localization_items(args.language_tag)
            print(items if not args.json else json.dumps({"content": items}))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
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
  # Moments and Content
  youversion votd                    # Get current day's verse
  youversion votd --day 100          # Get verse for day 100
  youversion moments --page 2       # Get moments from page 2
  youversion highlights --limit 5   # Show only 5 highlights
  youversion notes --json            # Output as JSON
  youversion bookmarks --page 1      # Get bookmarks from page 1
  youversion images --page 1         # Get images from page 1
  youversion badges --page 1         # Get badges from page 1
  youversion plan-progress           # Get plan progress
  youversion plan-subscriptions      # Get plan subscriptions
  youversion plan-completions        # Get plan completions
  youversion convert-notes           # Convert notes to markdown
  youversion create-moment --kind note --content "My note" --title "Title" --status private --body "Body" --color ff0000 --language-tag en --references "Genesis 1:1:1:GEN.1.1" --labels "test"

  # Bible and Audio
  youversion get-bible-configuration # Get Bible configuration
  youversion get-bible-versions --language-tag eng
  youversion get-bible-version 1     # Get version by ID
  youversion get-bible-chapter GEN.1 --version-id 1
  youversion get-audio-chapter GEN.1 --version-id 1
  youversion get-audio-version 1

  # Search
  youversion search-bible "love" --version-id 1
  youversion search-plans "daily" --language-tag en
  youversion search-users "john"

  # Videos
  youversion get-videos --language-tag eng
  youversion get-video-details 123

  # Events
  youversion search-events "church" --latitude 40.7128 --longitude -74.0060
  youversion get-event-details 123
  youversion get-saved-events
  youversion save-event 123
  youversion delete-saved-event 123

  # Themes
  youversion get-themes --language-tag eng
  youversion get-theme-description 1 --language-tag eng

  # Friends
  youversion send-friend-request 123456

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

    # Badges
    badges_parser = subparsers.add_parser("badges", help="Get badges")
    badges_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Bible API
    bible_config_parser = subparsers.add_parser(
        "get-bible-configuration", help="Get Bible configuration"
    )
    bible_versions_parser = subparsers.add_parser(
        "get-bible-versions", help="Get Bible versions"
    )
    bible_versions_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )
    bible_versions_parser.add_argument(
        "--version-type",
        type=str,
        default="all",
        dest="version_type",
        help="Version type: all, text, audio (default: all)",
    )
    bible_version_parser = subparsers.add_parser(
        "get-bible-version", help="Get specific Bible version"
    )
    bible_version_parser.add_argument("version_id", type=int, help="Version ID")
    bible_chapter_parser = subparsers.add_parser(
        "get-bible-chapter", help="Get Bible chapter"
    )
    bible_chapter_parser.add_argument(
        "reference", type=str, help="USFM reference (e.g., GEN.1)"
    )
    bible_chapter_parser.add_argument(
        "--version-id",
        type=int,
        default=1,
        dest="version_id",
        help="Version ID (default: 1)",
    )
    recommended_languages_parser = subparsers.add_parser(
        "get-recommended-languages", help="Get recommended languages"
    )
    recommended_languages_parser.add_argument(
        "--country", type=str, default="US", help="Country code (default: US)"
    )

    # Audio API
    audio_chapter_parser = subparsers.add_parser(
        "get-audio-chapter", help="Get audio chapter"
    )
    audio_chapter_parser.add_argument(
        "reference", type=str, help="USFM reference (e.g., GEN.1)"
    )
    audio_chapter_parser.add_argument(
        "--version-id",
        type=int,
        default=1,
        dest="version_id",
        help="Audio version ID (default: 1)",
    )
    audio_version_parser = subparsers.add_parser(
        "get-audio-version", help="Get audio version"
    )
    audio_version_parser.add_argument("audio_id", type=int, help="Audio version ID")

    # Search API
    search_bible_parser = subparsers.add_parser(
        "search-bible", help="Search Bible text"
    )
    search_bible_parser.add_argument("query", type=str, help="Search query")
    search_bible_parser.add_argument(
        "--version-id",
        type=int,
        default=None,
        dest="version_id",
        help="Version ID (optional)",
    )
    search_bible_parser.add_argument(
        "--book", type=str, default=None, help="Book filter (optional)"
    )
    search_bible_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    search_plans_parser = subparsers.add_parser(
        "search-plans", help="Search reading plans"
    )
    search_plans_parser.add_argument("query", type=str, help="Search query")
    search_plans_parser.add_argument(
        "--language-tag",
        type=str,
        default="en",
        dest="language_tag",
        help="Language tag (default: en)",
    )
    search_plans_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    search_users_parser = subparsers.add_parser("search-users", help="Search users")
    search_users_parser.add_argument("query", type=str, help="Search query")
    search_users_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )
    search_users_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Video API
    videos_parser = subparsers.add_parser("get-videos", help="Get videos")
    videos_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )
    video_details_parser = subparsers.add_parser(
        "get-video-details", help="Get video details"
    )
    video_details_parser.add_argument("video_id", type=int, help="Video ID")

    # Image API (different from my_images)
    get_images_parser = subparsers.add_parser(
        "get-images", help="Get images for a reference"
    )
    get_images_parser.add_argument("reference", type=str, help="USFM reference")
    get_images_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )
    get_images_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    image_upload_url_parser = subparsers.add_parser(
        "get-image-upload-url", help="Get image upload URL"
    )

    # Event API
    search_events_parser = subparsers.add_parser("search-events", help="Search events")
    search_events_parser.add_argument("query", type=str, help="Search query")
    search_events_parser.add_argument(
        "--latitude", type=float, default=None, help="Latitude (optional)"
    )
    search_events_parser.add_argument(
        "--longitude", type=float, default=None, help="Longitude (optional)"
    )
    search_events_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    event_details_parser = subparsers.add_parser(
        "get-event-details", help="Get event details"
    )
    event_details_parser.add_argument("event_id", type=int, help="Event ID")
    saved_events_parser = subparsers.add_parser(
        "get-saved-events", help="Get saved events"
    )
    saved_events_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    save_event_parser = subparsers.add_parser("save-event", help="Save event")
    save_event_parser.add_argument("event_id", type=int, help="Event ID")
    save_event_parser.add_argument(
        "--comments", type=str, default=None, help="Comments as JSON string (optional)"
    )
    delete_saved_event_parser = subparsers.add_parser(
        "delete-saved-event", help="Delete saved event"
    )
    delete_saved_event_parser.add_argument("event_id", type=int, help="Event ID")
    all_saved_event_ids_parser = subparsers.add_parser(
        "get-all-saved-event-ids", help="Get all saved event IDs"
    )
    event_config_parser = subparsers.add_parser(
        "get-event-configuration", help="Get event configuration"
    )

    # Moment management
    get_moments_parser = subparsers.add_parser("get-moments", help="Get moments list")
    get_moments_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    get_moments_parser.add_argument(
        "--user-id", type=int, default=None, dest="user_id", help="User ID (optional)"
    )
    get_moments_parser.add_argument(
        "--kind", type=str, default=None, help="Kind of moment (optional)"
    )
    get_moments_parser.add_argument(
        "--version-id",
        type=int,
        default=None,
        dest="version_id",
        help="Bible version ID (optional)",
    )
    get_moments_parser.add_argument(
        "--usfm", type=str, default=None, help="USFM reference (optional)"
    )
    moment_details_parser = subparsers.add_parser(
        "get-moment-details", help="Get moment details"
    )
    moment_details_parser.add_argument("moment_id", type=int, help="Moment ID")
    update_moment_parser = subparsers.add_parser("update-moment", help="Update moment")
    update_moment_parser.add_argument(
        "data", type=str, help="Moment data as JSON string"
    )
    delete_moment_parser = subparsers.add_parser("delete-moment", help="Delete moment")
    delete_moment_parser.add_argument("moment_id", type=int, help="Moment ID")
    moment_colors_parser = subparsers.add_parser(
        "get-moment-colors", help="Get moment colors"
    )
    moment_labels_parser = subparsers.add_parser(
        "get-moment-labels", help="Get moment labels"
    )
    verse_colors_parser = subparsers.add_parser(
        "get-verse-colors", help="Get verse colors"
    )
    verse_colors_parser.add_argument("usfm", type=str, help="USFM reference")
    verse_colors_parser.add_argument("version_id", type=int, help="Bible version ID")
    hide_verse_colors_parser = subparsers.add_parser(
        "hide-verse-colors", help="Hide verse colors"
    )
    hide_verse_colors_parser.add_argument(
        "data", type=str, help="Hide colors data as JSON string"
    )
    moments_config_parser = subparsers.add_parser(
        "get-moments-configuration", help="Get moments configuration"
    )

    # Comment API
    create_comment_parser = subparsers.add_parser(
        "create-comment", help="Create comment"
    )
    create_comment_parser.add_argument("moment_id", type=int, help="Moment ID")
    create_comment_parser.add_argument("comment", type=str, help="Comment text")
    delete_comment_parser = subparsers.add_parser(
        "delete-comment", help="Delete comment"
    )
    delete_comment_parser.add_argument("comment_id", type=int, help="Comment ID")

    # Like API
    like_moment_parser = subparsers.add_parser("like-moment", help="Like moment")
    like_moment_parser.add_argument("moment_id", type=int, help="Moment ID")
    unlike_moment_parser = subparsers.add_parser("unlike-moment", help="Unlike moment")
    unlike_moment_parser.add_argument("moment_id", type=int, help="Moment ID")

    # Device API
    register_device_parser = subparsers.add_parser(
        "register-device", help="Register device"
    )
    register_device_parser.add_argument("device_id", type=str, help="Device ID")
    register_device_parser.add_argument(
        "--device-type",
        type=str,
        default="android",
        dest="device_type",
        help="Device type (default: android)",
    )
    register_device_parser.add_argument(
        "--user-id", type=int, default=None, dest="user_id", help="User ID (optional)"
    )
    register_device_parser.add_argument(
        "--old-device-id",
        type=str,
        default=None,
        dest="old_device_id",
        help="Previous device ID (optional)",
    )
    register_device_parser.add_argument(
        "--tags", type=str, default=None, help="Device tags (optional)"
    )
    unregister_device_parser = subparsers.add_parser(
        "unregister-device", help="Unregister device"
    )
    unregister_device_parser.add_argument("device_id", type=str, help="Device ID")

    # Theme API
    themes_parser = subparsers.add_parser("get-themes", help="Get themes")
    themes_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )
    themes_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )
    add_theme_parser = subparsers.add_parser("add-theme", help="Add theme")
    add_theme_parser.add_argument("theme_id", type=int, help="Theme ID")
    add_theme_parser.add_argument(
        "--available-locales",
        type=str,
        required=True,
        dest="available_locales",
        help="Comma-separated locale codes",
    )
    add_theme_parser.add_argument(
        "--colors", type=str, required=True, help="Colors as JSON string"
    )
    add_theme_parser.add_argument(
        "--cta-urls",
        type=str,
        required=True,
        dest="cta_urls",
        help="CTA URLs as JSON string",
    )
    add_theme_parser.add_argument(
        "--msgid-suffix",
        type=str,
        required=True,
        dest="msgid_suffix",
        help="Message ID suffix",
    )
    add_theme_parser.add_argument(
        "--version-ids",
        type=str,
        required=True,
        dest="version_ids",
        help="Version IDs as JSON string",
    )
    remove_theme_parser = subparsers.add_parser("remove-theme", help="Remove theme")
    remove_theme_parser.add_argument("theme_id", type=int, help="Theme ID")
    set_theme_parser = subparsers.add_parser("set-theme", help="Set theme")
    set_theme_parser.add_argument("theme_id", type=int, help="Theme ID")
    set_theme_parser.add_argument(
        "--previous-theme-id",
        type=int,
        default=None,
        dest="previous_theme_id",
        help="Previous theme ID (optional)",
    )
    theme_description_parser = subparsers.add_parser(
        "get-theme-description", help="Get theme description"
    )
    theme_description_parser.add_argument("theme_id", type=int, help="Theme ID")
    theme_description_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
    )

    # Friend API
    send_friend_request_parser = subparsers.add_parser(
        "send-friend-request", help="Send friend request"
    )
    send_friend_request_parser.add_argument(
        "user_id", type=int, help="User ID to send friend request to"
    )

    # Localization API
    localization_parser = subparsers.add_parser(
        "get-localization-items", help="Get localization items"
    )
    localization_parser.add_argument(
        "--language-tag",
        type=str,
        default="eng",
        dest="language_tag",
        help="Language tag (default: eng)",
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
                "badges": badges_parser,
                "get-bible-configuration": bible_config_parser,
                "get-bible-versions": bible_versions_parser,
                "get-bible-version": bible_version_parser,
                "get-bible-chapter": bible_chapter_parser,
                "get-recommended-languages": recommended_languages_parser,
                "get-audio-chapter": audio_chapter_parser,
                "get-audio-version": audio_version_parser,
                "search-bible": search_bible_parser,
                "search-plans": search_plans_parser,
                "search-users": search_users_parser,
                "get-videos": videos_parser,
                "get-video-details": video_details_parser,
                "get-images": get_images_parser,
                "get-image-upload-url": image_upload_url_parser,
                "search-events": search_events_parser,
                "get-event-details": event_details_parser,
                "get-saved-events": saved_events_parser,
                "save-event": save_event_parser,
                "delete-saved-event": delete_saved_event_parser,
                "get-all-saved-event-ids": all_saved_event_ids_parser,
                "get-event-configuration": event_config_parser,
                "get-moments": get_moments_parser,
                "get-moment-details": moment_details_parser,
                "update-moment": update_moment_parser,
                "delete-moment": delete_moment_parser,
                "get-moment-colors": moment_colors_parser,
                "get-moment-labels": moment_labels_parser,
                "get-verse-colors": verse_colors_parser,
                "hide-verse-colors": hide_verse_colors_parser,
                "get-moments-configuration": moments_config_parser,
                "create-comment": create_comment_parser,
                "delete-comment": delete_comment_parser,
                "like-moment": like_moment_parser,
                "unlike-moment": unlike_moment_parser,
                "register-device": register_device_parser,
                "unregister-device": unregister_device_parser,
                "get-themes": themes_parser,
                "add-theme": add_theme_parser,
                "remove-theme": remove_theme_parser,
                "set-theme": set_theme_parser,
                "get-theme-description": theme_description_parser,
                "send-friend-request": send_friend_request_parser,
                "get-localization-items": localization_parser,
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
        "badges": cmd_badges,
        "get-bible-configuration": cmd_get_bible_configuration,
        "get-bible-versions": cmd_get_bible_versions,
        "get-bible-version": cmd_get_bible_version,
        "get-bible-chapter": cmd_get_bible_chapter,
        "get-recommended-languages": cmd_get_recommended_languages,
        "get-audio-chapter": cmd_get_audio_chapter,
        "get-audio-version": cmd_get_audio_version,
        "search-bible": cmd_search_bible,
        "search-plans": cmd_search_plans,
        "search-users": cmd_search_users,
        "get-videos": cmd_get_videos,
        "get-video-details": cmd_get_video_details,
        "get-images": cmd_get_images,
        "get-image-upload-url": cmd_get_image_upload_url,
        "search-events": cmd_search_events,
        "get-event-details": cmd_get_event_details,
        "get-saved-events": cmd_get_saved_events,
        "save-event": cmd_save_event,
        "delete-saved-event": cmd_delete_saved_event,
        "get-all-saved-event-ids": cmd_get_all_saved_event_ids,
        "get-event-configuration": cmd_get_event_configuration,
        "get-moments": cmd_get_moments,
        "get-moment-details": cmd_get_moment_details,
        "update-moment": cmd_update_moment,
        "delete-moment": cmd_delete_moment,
        "get-moment-colors": cmd_get_moment_colors,
        "get-moment-labels": cmd_get_moment_labels,
        "get-verse-colors": cmd_get_verse_colors,
        "hide-verse-colors": cmd_hide_verse_colors,
        "get-moments-configuration": cmd_get_moments_configuration,
        "create-comment": cmd_create_comment,
        "delete-comment": cmd_delete_comment,
        "like-moment": cmd_like_moment,
        "unlike-moment": cmd_unlike_moment,
        "register-device": cmd_register_device,
        "unregister-device": cmd_unregister_device,
        "get-themes": cmd_get_themes,
        "add-theme": cmd_add_theme,
        "remove-theme": cmd_remove_theme,
        "set-theme": cmd_set_theme,
        "get-theme-description": cmd_get_theme_description,
        "send-friend-request": cmd_send_friend_request,
        "get-localization-items": cmd_get_localization_items,
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




if __name__ == "__main__":
    main()
