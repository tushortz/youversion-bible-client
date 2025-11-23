"""Bible-related data models."""

from typing import Any, Optional, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing_extensions import TypeAlias


class LanguageProtocol(Protocol):
    """Protocol for language information."""

    id: int
    name: str
    language_tag: str
    local_name: Optional[str]

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
    url: Optional[str]

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
    testament: Optional[str]

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
    copyright_short: Optional[str]
    copyright_long: Optional[str]
    local_title: Optional[str]
    local_abbreviation: Optional[str]
    language_tag_selected: Optional[str]
    last_modified: Optional[int]
    metadata_build: Optional[int]
    reader_footer: Optional[str]
    reader_footer_url: Optional[str]

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
    stylesheets: Optional[list[dict]]

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
