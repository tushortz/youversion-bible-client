"""Unit tests for URLDiscovery class."""

from unittest.mock import AsyncMock, patch

import pytest

from youversion.config import Config
from youversion.core.url_discovery import URLDiscovery


class TestURLDiscovery:
    """Test cases for URLDiscovery class."""

    @pytest.mark.asyncio
    async def test_discover_endpoints(self):
        """Test endpoint discovery."""
        username = "testuser"
        endpoints = await URLDiscovery.discover_endpoints(username)

        expected = {
            "reading_plans": f"{Config.BIBLE_COM_BASE_URL}/users/{username}/reading-plans",
            "user_profile": f"{Config.BIBLE_COM_BASE_URL}/users/{username}",
            "moments": f"{Config.BASE_URL}/users/{username}/_cards.json",
            "verse_of_the_day": Config.VOTD_URL,
        }

        assert endpoints == expected

    @pytest.mark.asyncio
    async def test_test_endpoint_success(self):
        """Test endpoint testing with successful response."""
        url = "https://example.com/test"

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/json"}

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            result = await URLDiscovery.test_endpoint(url)

            expected = {
                "url": url,
                "status_code": 200,
                "accessible": True,
                "content_type": "application/json",
                "requires_auth": False,
                "redirects": False,
                "redirect_url": None,
            }

            assert result == expected

    @pytest.mark.asyncio
    async def test_test_endpoint_redirect(self):
        """Test endpoint testing with redirect response."""
        url = "https://example.com/test"
        redirect_url = "https://example.com/redirected"

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 301
            mock_response.headers = {"location": redirect_url}

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            result = await URLDiscovery.test_endpoint(url)

            expected = {
                "url": url,
                "status_code": 301,
                "accessible": True,
                "content_type": "",
                "requires_auth": False,
                "redirects": True,
                "redirect_url": redirect_url,
            }

            assert result == expected

    @pytest.mark.asyncio
    async def test_test_endpoint_auth_required(self):
        """Test endpoint testing with authentication required."""
        url = "https://example.com/test"

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 401
            mock_response.headers = {}

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            result = await URLDiscovery.test_endpoint(url)

            expected = {
                "url": url,
                "status_code": 401,
                "accessible": False,
                "content_type": "",
                "requires_auth": True,
                "redirects": False,
                "redirect_url": None,
            }

            assert result == expected

    @pytest.mark.asyncio
    async def test_test_endpoint_error(self):
        """Test endpoint testing with network error."""
        url = "https://example.com/test"

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = (
                Exception("Network error")
            )

            result = await URLDiscovery.test_endpoint(url)

            expected = {
                "url": url,
                "status_code": None,
                "accessible": False,
                "error": "Network error",
            }

            assert result == expected

    @pytest.mark.asyncio
    async def test_discover_working_endpoints(self):
        """Test discovering working endpoints for a user."""
        username = "testuser"

        # Mock the discover_endpoints method
        mock_endpoints = {
            "reading_plans": "https://example.com/reading-plans",
            "user_profile": "https://example.com/profile",
        }

        # Mock the test_endpoint method
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

        def mock_test_endpoint(url, headers=None):
            # Extract endpoint name from URL
            if "reading-plans" in url:
                return mock_results["reading_plans"]
            elif "profile" in url:
                return mock_results["user_profile"]
            return None

        with patch.object(
            URLDiscovery, "discover_endpoints", return_value=mock_endpoints
        ), patch.object(URLDiscovery, "test_endpoint", side_effect=mock_test_endpoint):
            results = await URLDiscovery.discover_working_endpoints(username)

            assert len(results) == 2
            assert "reading_plans" in results
            assert "user_profile" in results
            assert results["reading_plans"]["accessible"] is True
            assert results["user_profile"]["accessible"] is False
