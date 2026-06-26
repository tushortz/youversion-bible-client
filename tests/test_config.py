"""Unit tests for Config class."""

from youversion.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_constants(self):
        """Test that all constants are properly defined."""
        assert Config.BASE_URL == "https://my.bible.com"
        assert Config.BIBLE_COM_BASE_URL == "https://www.bible.com"
        assert Config.VOTD_URL == "https://nodejs.bible.com/api/moments/votd/3.1"
        assert Config.AUTH_URL == "https://auth.youversionapi.com/token"
        assert Config.CLIENT_ID == "ODViNjFkOTdhNzliOTZiZTQ2NWViYWVlZTgzYjEzMTM="
        assert Config.CLIENT_SECRET == "NzVjZjBlMTQxY2JmNDFlZjQxMGFkY2U1YjY1MzdhNDk="
        assert Config.SIGNIN_URL == "/sign-in"
        assert Config.READING_PLANS_URL == "/users/{username}/reading-plans"
        assert Config.USER_PROFILE_URL == "/users/{username}"
        assert Config.HTTP_TIMEOUT == 30.0
        assert Config.DEFAULT_PAGE == 1
        assert Config.DEFAULT_LIMIT == 10
