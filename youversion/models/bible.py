"""Bible-related data models."""

from typing import Any, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing import TypeAlias


class LanguageProtocol(Protocol):
    """Protocol for language information."""

    id: int
    name: str
    language_tag: str
    local_name: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Language: TypeAlias = LanguageProtocol


class PublisherProtocol(Protocol):
    """Protocol for publisher information."""

    id: int
    name: str
    url: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Publisher: TypeAlias = PublisherProtocol


class BookProtocol(Protocol):
    """Protocol for Bible book information."""

    id: int
    name: str
    abbreviation: str
    chapters: list[int]
    testament: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Book: TypeAlias = BookProtocol


class VersionProtocol(Protocol):
    """Protocol for Bible version information."""

    id: int
    title: str
    abbreviation: str
    language: Language
    publisher: Publisher
    books: list[Book]
    text: bool
    audio: bool
    copyright_short: str | None
    copyright_long: str | None
    local_title: str | None
    local_abbreviation: str | None
    language_tag_selected: str | None
    last_modified: int | None
    metadata_build: int | None
    reader_footer: str | None
    reader_footer_url: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Version: TypeAlias = VersionProtocol


class ChapterProtocol(Protocol):
    """Protocol for chapter information."""

    usfm: str
    human: str
    canonical: bool
    toc: bool

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Chapter: TypeAlias = ChapterProtocol


class ChapterContentProtocol(Protocol):
    """Protocol for chapter content with verses."""

    id: int
    reference: str
    content: str
    verses: list[str]
    chapters: list[Chapter]
    version: Version

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
ChapterContent: TypeAlias = ChapterContentProtocol


class ConfigurationProtocol(Protocol):
    """Protocol for Bible configuration."""

    versions: list[Version]
    languages: list[Language]
    stylesheets: list[dict] | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Configuration: TypeAlias = ConfigurationProtocol


class RecommendedLanguagesProtocol(Protocol):
    """Protocol for recommended languages for a country."""

    languages: list[Language]
    country: str

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
RecommendedLanguages: TypeAlias = RecommendedLanguagesProtocol
