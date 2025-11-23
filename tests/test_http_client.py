"""Unit tests for HttpClient class."""

from unittest.mock import AsyncMock

import pytest

from youversion.config import Config
from youversion.core.http_client import HttpClient


class TestHttpClient:
    """Test cases for HttpClient class."""

    def test_init(self):
        """Test HttpClient initialization."""
        mock_client = AsyncMock()
        http_client = HttpClient(mock_client)

        assert http_client._client == mock_client

    @pytest.mark.asyncio
    async def test_get_success(self):
        """Test successful GET request."""
        url = "https://example.com/test"
        mock_response_data = {"key": "value"}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.get(url)

        assert result == mock_response_data
        mock_client.get.assert_called_once_with(url)

    @pytest.mark.asyncio
    async def test_get_with_params(self):
        """Test GET request with parameters."""
        url = "https://example.com/test"
        params = {"page": 1, "limit": 10}
        mock_response_data = {"data": "test"}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.get(url, params=params)

        assert result == mock_response_data
        mock_client.get.assert_called_once_with(url, params=params)

    @pytest.mark.asyncio
    async def test_post_success(self):
        """Test successful POST request."""
        url = "https://example.com/test"
        data = {"key": "value"}
        mock_response_data = {"success": True}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.post = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.post(url, data=data)

        assert result == mock_response_data
        mock_client.post.assert_called_once_with(url, data=data)

    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing HTTP client."""
        mock_client = AsyncMock()

        http_client = HttpClient(mock_client)
        await http_client.close()

        mock_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_with_none_client(self):
        """Test closing HTTP client when client is None."""
        http_client = HttpClient(None)

        # Should not raise an exception
        await http_client.close()

    @pytest.mark.asyncio
    async def test_get_cards_success(self):
        """Test successful get_cards request."""
        user_id = 123
        page = 2
        kind = "highlights"
        mock_response_data = {"moments": [{"id": 1, "type": "highlight"}]}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client, user_id=user_id)
        result = await http_client.get_cards(page=page, kind=kind)

        assert result == mock_response_data

        # Verify URL construction and params
        from youversion.config import Config
        expected_url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_ITEMS_URL}"
        expected_params = {"page": page, "kind": kind, "user_id": user_id}
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == expected_url
        # Check params (headers are merged with DEFAULT_HEADERS)
        actual_params = call_args[1].get("params", {})
        assert actual_params["page"] == expected_params["page"]
        assert actual_params["kind"] == expected_params["kind"]
        assert actual_params["user_id"] == expected_params["user_id"]

    @pytest.mark.asyncio
    async def test_get_cards_default_params(self):
        """Test get_cards request with default parameters."""
        user_id = 123
        mock_response_data = {"moments": []}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client, user_id=user_id)
        result = await http_client.get_cards()

        assert result == mock_response_data

        # Verify default parameters
        from youversion.config import Config
        expected_url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_ITEMS_URL}"
        expected_params = {"page": 1, "user_id": user_id}
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == expected_url
        # Check params (headers are merged with DEFAULT_HEADERS)
        actual_params = call_args[1].get("params", {})
        assert actual_params["page"] == expected_params["page"]
        assert actual_params["user_id"] == expected_params["user_id"]

    @pytest.mark.asyncio
    async def test_get_verse_of_the_day_success(self):
        """Test successful get_verse_of_the_day request."""
        mock_response_data = {"day": 1, "usfm": "JHN.3.16", "image_id": "test_image"}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.get_verse_of_the_day()

        assert result == mock_response_data
        mock_client.get.assert_called_once_with(Config.VOTD_URL)

    @pytest.mark.asyncio
    async def test_get_json_error(self):
        """Test GET request with JSON parsing error."""
        url = "https://example.com/test"

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(side_effect=ValueError("Invalid JSON"))
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)

        with pytest.raises(ValueError, match="Invalid JSON"):
            await http_client.get(url)

    @pytest.mark.asyncio
    async def test_post_json_error(self):
        """Test POST request with JSON parsing error."""
        url = "https://example.com/test"
        data = {"key": "value"}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(side_effect=ValueError("Invalid JSON"))
        mock_client.post = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)

        with pytest.raises(ValueError, match="Invalid JSON"):
            await http_client.post(url, data=data)

    @pytest.mark.asyncio
    async def test_get_cards_json_error(self):
        """Test get_cards request with JSON parsing error."""
        user_id = 123

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(side_effect=ValueError("Invalid JSON"))
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client, user_id=user_id)

        with pytest.raises(ValueError, match="Invalid JSON"):
            await http_client.get_cards()

    @pytest.mark.asyncio
    async def test_get_verse_of_the_day_json_error(self):
        """Test get_verse_of_the_day request with JSON parsing error."""
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(side_effect=ValueError("Invalid JSON"))
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)

        with pytest.raises(ValueError, match="Invalid JSON"):
            await http_client.get_verse_of_the_day()

    @pytest.mark.asyncio
    async def test_close_error(self):
        """Test closing HTTP client with error."""
        mock_client = AsyncMock()
        mock_client.aclose.side_effect = Exception("Close error")

        http_client = HttpClient(mock_client)

        with pytest.raises(Exception, match="Close error"):
            await http_client.close()
