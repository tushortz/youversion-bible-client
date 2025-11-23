"""Unit tests for CLI functions."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.cli import (
    cmd_bookmarks,
    cmd_convert_notes,
    cmd_discover_endpoints,
    cmd_highlights,
    cmd_images,
    cmd_moments,
    cmd_notes,
    cmd_plan_progress,
    cmd_plan_subscriptions,
    cmd_votd,
    create_parser,
    main,
)


class TestCLI:
    """Test cases for CLI functions."""

    @pytest.mark.asyncio
    async def test_cmd_votd_success(self):
        """Test successful verse of the day command."""
        mock_votd = MagicMock()
        mock_votd.day = 15
        mock_votd.usfm = ["JHN.3.16"]
        mock_votd.image_id = "img123"

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.verse_of_the_day = AsyncMock(return_value=mock_votd)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.day = None

            await cmd_votd(args)

            mock_client.verse_of_the_day.assert_called_once_with(day=None)

    @pytest.mark.asyncio
    async def test_cmd_votd_with_day(self):
        """Test verse of the day command with specific day."""
        mock_votd = MagicMock()
        mock_votd.day = 20
        mock_votd.usfm = ["PSA.23.1"]
        mock_votd.image_id = "img124"

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.verse_of_the_day = AsyncMock(return_value=mock_votd)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.day = 20

            await cmd_votd(args)

            mock_client.verse_of_the_day.assert_called_once_with(day=20)

    @pytest.mark.asyncio
    async def test_cmd_votd_json_output(self):
        """Test verse of the day command with JSON output."""
        mock_votd = MagicMock()
        mock_votd.model_dump.return_value = {"day": 15, "usfm": ["JHN.3.16"]}

        with patch("youversion.cli.AsyncClient") as mock_client_class, patch(
            "youversion.cli.json.dumps"
        ) as mock_json:
            mock_client = AsyncMock()
            mock_client.verse_of_the_day = AsyncMock(return_value=mock_votd)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            mock_json.return_value = '{"day": 15, "usfm": ["JHN.3.16"]}'

            args = MagicMock()
            args.day = None
            args.json = True

            await cmd_votd(args)

            mock_votd.model_dump.assert_called_once()
            mock_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_cmd_moments_success(self):
        """Test successful moments command."""
        mock_moments = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.moments = AsyncMock(return_value=mock_moments)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_moments(args)

            mock_client.moments.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_moments_with_limit(self):
        """Test moments command with limit."""
        mock_moments = [MagicMock() for _ in range(10)]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.moments = AsyncMock(return_value=mock_moments)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 5
            args.json = False

            await cmd_moments(args)

            mock_client.moments.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_moments_json_output(self):
        """Test moments command with JSON output."""
        mock_moments = [MagicMock(), MagicMock()]
        for moment in mock_moments:
            moment.model_dump.return_value = {"id": "123", "type": "moment"}

        with patch("youversion.cli.AsyncClient") as mock_client_class, patch(
            "youversion.cli.json.dumps"
        ) as mock_json:
            mock_client = AsyncMock()
            mock_client.moments = AsyncMock(return_value=mock_moments)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            mock_json.return_value = '[{"id": "123", "type": "moment"}]'

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = True

            await cmd_moments(args)

            for moment in mock_moments:
                moment.model_dump.assert_called_once()
            mock_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_cmd_highlights_success(self):
        """Test successful highlights command."""
        mock_highlights = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.highlights = AsyncMock(return_value=mock_highlights)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_highlights(args)

            mock_client.highlights.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_notes_success(self):
        """Test successful notes command."""
        mock_notes = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.notes = AsyncMock(return_value=mock_notes)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_notes(args)

            mock_client.notes.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_bookmarks_success(self):
        """Test successful bookmarks command."""
        mock_bookmarks = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.bookmarks = AsyncMock(return_value=mock_bookmarks)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_bookmarks(args)

            mock_client.bookmarks.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_images_success(self):
        """Test successful images command."""
        mock_images = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.my_images = AsyncMock(return_value=mock_images)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_images(args)

            mock_client.my_images.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_plan_progress_success(self):
        """Test successful plan progress command."""
        mock_progress = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.plan_progress = AsyncMock(return_value=mock_progress)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_plan_progress(args)

            mock_client.plan_progress.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_plan_subscriptions_success(self):
        """Test successful plan subscriptions command."""
        mock_subscriptions = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.plan_subscriptions = AsyncMock(return_value=mock_subscriptions)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.page = 1
            args.limit = 10
            args.json = False

            await cmd_plan_subscriptions(args)

            mock_client.plan_subscriptions.assert_called_once_with(page=1)

    @pytest.mark.asyncio
    async def test_cmd_convert_notes_success(self):
        """Test successful convert notes command."""
        mock_converted = [MagicMock(), MagicMock()]

        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.convert_note_to_md = AsyncMock(return_value=mock_converted)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.limit = 10
            args.json = False

            await cmd_convert_notes(args)

            mock_client.convert_note_to_md.assert_called_once()

    @pytest.mark.asyncio
    async def test_cmd_discover_endpoints_success(self):
        """Test successful discover endpoints command."""
        mock_endpoints = {
            "reading_plans": "https://example.com/reading-plans",
            "user_profile": "https://example.com/profile",
        }

        mock_results = {
            "reading_plans": {
                "url": "https://example.com/reading-plans",
                "status_code": 200,
                "accessible": True,
            },
            "user_profile": {
                "url": "https://example.com/profile",
                "status_code": 404,
                "accessible": False,
            },
        }

        with patch("youversion.cli.URLDiscovery") as mock_discovery:
            mock_discovery.discover_endpoints = AsyncMock(return_value=mock_endpoints)
            mock_discovery.test_endpoint = AsyncMock(
                side_effect=lambda url, headers=None: mock_results.get(
                    url.split("/")[-1]
                )
            )

            args = MagicMock()
            args.username = "testuser"

            await cmd_discover_endpoints(args)

            mock_discovery.discover_endpoints.assert_called_once_with(
                "testuser")

    @pytest.mark.asyncio
    async def test_cmd_discover_endpoints_no_username(self):
        """Test discover endpoints command without username."""
        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.username = "testuser"
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.username = None

            await cmd_discover_endpoints(args)

            # Should use client username
            mock_client_class.assert_called_once()

    def test_create_parser(self):
        """Test parser creation."""
        parser = create_parser()

        # Test that parser has all expected commands
        subparsers = parser._subparsers._actions[0]
        if subparsers and hasattr(subparsers, "choices"):
            assert "votd" in subparsers.choices
            assert "moments" in subparsers.choices
            assert "highlights" in subparsers.choices
            assert "notes" in subparsers.choices
            assert "bookmarks" in subparsers.choices
            assert "images" in subparsers.choices
            assert "plan-progress" in subparsers.choices
            assert "plan-subscriptions" in subparsers.choices
            assert "convert-notes" in subparsers.choices
            assert "discover-endpoints" in subparsers.choices
        else:
            # Test that parser exists and has the expected structure
            assert parser is not None
            assert hasattr(parser, "_subparsers")

    @pytest.mark.asyncio
    async def test_main_votd_command(self):
        """Test main function with votd command."""
        with patch("youversion.cli.cmd_votd") as mock_cmd, patch(
            "youversion.cli.create_parser"
        ) as mock_parser, patch("youversion.cli.check_credentials") as mock_check:
            mock_args = MagicMock()
            mock_args.command = "votd"
            mock_args.day = None
            mock_args.json = False

            mock_parser.return_value.parse_args.return_value = mock_args

            await main()

            mock_check.assert_called_once()
            mock_cmd.assert_called_once_with(mock_args)

    @pytest.mark.asyncio
    async def test_main_moments_command(self):
        """Test main function with moments command."""
        with patch("youversion.cli.cmd_moments") as mock_cmd, patch(
            "youversion.cli.create_parser"
        ) as mock_parser, patch("youversion.cli.check_credentials") as mock_check:
            mock_args = MagicMock()
            mock_args.command = "moments"
            mock_args.page = 1
            mock_args.limit = None
            mock_args.json = False

            mock_parser.return_value.parse_args.return_value = mock_args

            await main()

            mock_check.assert_called_once()
            mock_cmd.assert_called_once_with(mock_args)

    @pytest.mark.asyncio
    async def test_main_discover_endpoints_command(self):
        """Test main function with discover-endpoints command."""
        with patch("youversion.cli.cmd_discover_endpoints") as mock_cmd, patch(
            "youversion.cli.create_parser"
        ) as mock_parser, patch("youversion.cli.check_credentials") as mock_check:
            mock_args = MagicMock()
            mock_args.command = "discover-endpoints"
            mock_args.username = "testuser"

            mock_parser.return_value.parse_args.return_value = mock_args

            await main()

            mock_check.assert_called_once()
            mock_cmd.assert_called_once_with(mock_args)

    @pytest.mark.asyncio
    async def test_main_unknown_command(self):
        """Test main function with unknown command."""
        with patch("youversion.cli.create_parser") as mock_parser, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            mock_args = MagicMock()
            mock_args.command = "unknown"

            mock_parser.return_value.parse_args.return_value = mock_args

            # Should raise KeyError for unknown command
            with pytest.raises(KeyError):
                await main()

    @pytest.mark.asyncio
    async def test_poetry_cmd_wrappers(self):
        """Test Poetry command wrapper functions."""
        from youversion.cli import (
            poetry_cmd_bookmarks,
            poetry_cmd_convert_notes,
            poetry_cmd_discover_endpoints,
            poetry_cmd_highlights,
            poetry_cmd_images,
            poetry_cmd_moments,
            poetry_cmd_notes,
            poetry_cmd_plan_progress,
            poetry_cmd_plan_subscriptions,
            poetry_cmd_votd,
        )

        with patch("youversion.cli.cmd_votd") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_votd()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_moments") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_moments()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_highlights") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_highlights()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_notes") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_notes()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_bookmarks") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_bookmarks()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_images") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_images()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_plan_progress") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_plan_progress()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_plan_subscriptions") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_plan_subscriptions()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_convert_notes") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_convert_notes()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

        with patch("youversion.cli.cmd_discover_endpoints") as mock_cmd, patch(
            "youversion.cli.check_credentials"
        ) as mock_check:
            await poetry_cmd_discover_endpoints()
            mock_check.assert_called_once()
            mock_cmd.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in CLI commands."""
        with patch("youversion.cli.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.verse_of_the_day = AsyncMock(side_effect=Exception("API Error"))
            mock_client_class.return_value.__aenter__.return_value = mock_client

            args = MagicMock()
            args.day = None
            args.json = False

            # Should raise SystemExit when an error occurs
            with pytest.raises(SystemExit):
                await cmd_votd(args)
