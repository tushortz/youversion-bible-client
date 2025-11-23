"""URL discovery utilities for YouVersion API endpoints."""

from typing import Optional

import httpx

from ..config import Config


class URLDiscovery:
    """Utilities for discovering YouVersion API endpoints and build IDs."""


    @staticmethod
    async def discover_endpoints(username: str) -> dict[str, str]:
        """Discover available API endpoints for a user.

        Args:
            username: The username to discover endpoints for

        Returns:
            Dictionary of endpoint names to URLs
        """
        endpoints = {
            "reading_plans": f"{Config.BIBLE_COM_BASE_URL}/users/{username}/reading-plans",
            "user_profile": f"{Config.BIBLE_COM_BASE_URL}/users/{username}",
            "moments": f"{Config.BASE_URL}/users/{username}/_cards.json",
            "verse_of_the_day": Config.VOTD_URL,
        }

        return endpoints

    @staticmethod
    async def test_endpoint(
        url: str, headers: Optional[dict[str, str]] = None
    ) -> dict[str, any]:
        """Test if an endpoint is accessible and return response info.

        Args:
            url: URL to test
            headers: Optional headers to send

        Returns:
            Dictionary with response info
        """
        try:
            async with httpx.AsyncClient(timeout=Config.HTTP_TIMEOUT) as client:
                response = await client.get(url, headers=headers or {})

                return {
                    "url": url,
                    "status_code": response.status_code,
                    "accessible": response.status_code < 400,
                    "content_type": response.headers.get("content-type", ""),
                    "requires_auth": response.status_code == 401
                    or response.status_code == 403,
                    "redirects": response.status_code in [301, 302, 307, 308],
                    "redirect_url": response.headers.get("location")
                    if response.status_code in [301, 302, 307, 308]
                    else None,
                }

        except Exception as e:
            return {
                "url": url,
                "status_code": None,
                "accessible": False,
                "error": str(e),
            }

    @staticmethod
    async def discover_working_endpoints(
        username: str, auth_headers: Optional[dict[str, str]] = None
    ) -> dict[str, dict[str, any]]:
        """Discover which endpoints are working for a user.

        Args:
            username: The username to test endpoints for
            auth_headers: Optional authentication headers

        Returns:
            Dictionary of endpoint names to test results
        """
        endpoints = await URLDiscovery.discover_endpoints(username)
        results = {}

        for name, url in endpoints.items():
            results[name] = await URLDiscovery.test_endpoint(url, auth_headers)

        return results
