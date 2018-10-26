"""Unit tests for BaseClient class."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.core.base_client import BaseClient
from youversion.enums import MomentKinds


class TestBaseClient:
    """Test cases for BaseClient class."""

    def test_init_with_credentials(self):
        """Test initializing base client with explicit credentials."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password
            mock_auth_class.return_value = mock_auth

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)

            assert client._authenticator == mock_auth
            assert client._data_processor == mock_processor
            assert client._http_client is None
            mock_auth_class.assert_called_once_with(username, password)

    def test_init_without_credentials(self):
        """Test initializing base client without explicit credentials."""
        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth_class.return_value = mock_auth

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient()

            assert client._authenticator == mock_auth
            assert client._data_processor == mock_processor
            assert client._http_client is None
            mock_auth_class.assert_called_once_with(None, None)

    @pytest.mark.asyncio
    async def test_ensure_authenticated_success(self):
        """Test successful authentication."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class, patch(
            "youversion.core.base_client.HttpClient"
        ) as mock_http_class:
            mock_auth = AsyncMock()
            mock_auth.username = username
            mock_auth.password = password
            mock_auth.authenticate = AsyncMock()

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_class.return_value = mock_http_client

            mock_auth_client = AsyncMock()
            mock_auth.authenticate.return_value = mock_auth_client

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth

            await client._ensure_authenticated()

            assert client._http_client == mock_http_client
            mock_auth.authenticate.assert_called_once_with(username, password)
            mock_http_class.assert_called_once_with(mock_auth_client)

    @pytest.mark.asyncio
    async def test_ensure_authenticated_already_authenticated(self):
        """Test authentication when already authenticated."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = AsyncMock()  # Already authenticated

            await client._ensure_authenticated()

            # Should not call authenticate again
            assert (
                not hasattr(mock_auth, "authenticate")
                or not mock_auth.authenticate.called
            )

    @pytest.mark.asyncio
    async def test_get_cards_data_success(self):
        """Test successful cards data retrieval."""
        username = "testuser"
        password = "testpass"
        kind = "highlights"
        page = 2
        mock_data = [{"id": "1", "type": "highlight"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client._get_cards_data(kind=kind, page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=kind
            )

    @pytest.mark.asyncio
    async def test_moments_success(self):
        """Test successful moments retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_raw_data = [{"kind": "highlight", "object": {"id": "1"}}]
        mock_processed_data = [MagicMock()]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor.process_moments.return_value = mock_processed_data
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_raw_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.moments(page=page)

            assert result == mock_processed_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=""
            )
            mock_processor.process_moments.assert_called_once_with(mock_raw_data)

    @pytest.mark.asyncio
    async def test_highlights_success(self):
        """Test successful highlights retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_raw_data = [{"kind": "highlight", "object": {"id": "1"}}]
        mock_processed_data = [MagicMock()]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor.process_highlights.return_value = mock_processed_data
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_raw_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.highlights(page=page)

            assert result == mock_processed_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.HIGHLIGHT.value
            )
            mock_processor.process_highlights.assert_called_once_with(mock_raw_data)

    @pytest.mark.asyncio
    async def test_verse_of_the_day_success(self):
        """Test successful verse of the day retrieval."""
        username = "testuser"
        password = "testpass"
        day = 15
        mock_raw_data = {"votd": [{"day": 15, "usfm": "JHN.3.16"}]}
        mock_processed_data = MagicMock()

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor.process_verse_of_the_day.return_value = mock_processed_data
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_verse_of_the_day = AsyncMock(
                return_value=mock_raw_data
            )

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.verse_of_the_day(day=day)

            assert result == mock_processed_data
            mock_http_client.get_verse_of_the_day.assert_called_once()
            mock_processor.process_verse_of_the_day.assert_called_once_with(
                mock_raw_data, day
            )

    @pytest.mark.asyncio
    async def test_notes_success(self):
        """Test successful notes retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_data = [{"id": "1", "type": "note"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.notes(page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.NOTE.value
            )

    @pytest.mark.asyncio
    async def test_bookmarks_success(self):
        """Test successful bookmarks retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_data = [{"id": "1", "type": "bookmark"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.bookmarks(page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.BOOKMARK.value
            )

    @pytest.mark.asyncio
    async def test_my_images_success(self):
        """Test successful images retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_data = [{"id": "1", "type": "image"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.my_images(page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.IMAGE.value
            )

    @pytest.mark.asyncio
    async def test_plan_progress_success(self):
        """Test successful plan progress retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_data = [{"id": "1", "type": "plan_progress"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.plan_progress(page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.PLAN_SEGMENT_COMPLETION.value
            )

    @pytest.mark.asyncio
    async def test_plan_subscriptions_success(self):
        """Test successful plan subscriptions retrieval."""
        username = "testuser"
        password = "testpass"
        page = 1
        mock_data = [{"id": "1", "type": "plan_subscription"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.plan_subscriptions(page=page)

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=page, kind=MomentKinds.PLAN_SUBSCRIPTION.value
            )

    @pytest.mark.asyncio
    async def test_convert_note_to_md_success(self):
        """Test successful note to markdown conversion."""
        username = "testuser"
        password = "testpass"
        mock_data = [{"id": "1", "type": "note"}]

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.get_cards = AsyncMock(return_value=mock_data)

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            result = await client.convert_note_to_md()

            assert result == mock_data
            mock_http_client.get_cards.assert_called_once_with(
                username, page=1, kind=MomentKinds.NOTE.value
            )

    @pytest.mark.asyncio
    async def test_close_success(self):
        """Test successful client closure."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            mock_http_client = AsyncMock()
            mock_http_client.close = AsyncMock()

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = mock_http_client

            await client.close()

            mock_http_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_no_http_client(self):
        """Test client closure when no HTTP client exists."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth
            client._http_client = None

            # Should not raise an exception
            await client.close()

    def test_username_property(self):
        """Test username property."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth

            assert client.username == username
