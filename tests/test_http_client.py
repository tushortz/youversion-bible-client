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
        username = "testuser"
        page = 2
        kind = "highlights"
        mock_response_data = {"cards": [{"id": 1, "type": "highlight"}]}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.get_cards(username, page=page, kind=kind)

        assert result == mock_response_data

        # Verify URL construction
        expected_url = (
            f"{Config.BASE_URL}{Config.MOMENTS_URL.format(username=username)}"
        )
        expected_params = {"page": page, "kind": kind}
        mock_client.get.assert_called_once_with(expected_url, params=expected_params)

    @pytest.mark.asyncio
    async def test_get_cards_default_params(self):
        """Test get_cards request with default parameters."""
        username = "testuser"
        mock_response_data = {"cards": []}

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)
        result = await http_client.get_cards(username)

        assert result == mock_response_data

        # Verify default parameters
        expected_url = (
            f"{Config.BASE_URL}{Config.MOMENTS_URL.format(username=username)}"
        )
        expected_params = {"page": 1, "kind": ""}
        mock_client.get.assert_called_once_with(expected_url, params=expected_params)

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
        username = "testuser"

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(side_effect=ValueError("Invalid JSON"))
        mock_client.get = AsyncMock(return_value=mock_response)

        http_client = HttpClient(mock_client)

        with pytest.raises(ValueError, match="Invalid JSON"):
            await http_client.get_cards(username)

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
