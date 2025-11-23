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
        assert Config.CLIENT_ID == "85b61d97a79b96be465ebaeee83b1313"
        assert Config.CLIENT_SECRET == "75cf0e141cbf41ef410adce5b6537a49"
        assert Config.SIGNIN_URL == "/sign-in"
        assert Config.READING_PLANS_URL == "/users/{username}/reading-plans"
        assert Config.USER_PROFILE_URL == "/users/{username}"
        assert Config.HTTP_TIMEOUT == 30.0
        assert Config.DEFAULT_PAGE == 1
        assert Config.DEFAULT_LIMIT == 10
