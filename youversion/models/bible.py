"""Bible-related data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Language:
    """Language information."""
    id: int
    name: str
    language_tag: str
    local_name: Optional[str] = None


@dataclass
class Publisher:
    """Publisher information."""
    id: int
    name: str
    url: Optional[str] = None


@dataclass
class Book:
    """Bible book information."""
    id: int
    name: str
    abbreviation: str
    chapters: List[int]
    testament: Optional[str] = None


@dataclass
class Version:
    """Bible version information."""
    id: int
    title: str
    abbreviation: str
    language: Language
    publisher: Publisher
    books: List[Book]
    text: bool = True
    audio: bool = False
    copyright_short: Optional[str] = None
    copyright_long: Optional[str] = None
    local_title: Optional[str] = None
    local_abbreviation: Optional[str] = None
    language_tag_selected: Optional[str] = None
    last_modified: Optional[int] = None
    metadata_build: Optional[int] = None
    reader_footer: Optional[str] = None
    reader_footer_url: Optional[str] = None


@dataclass
class Chapter:
    """Chapter information."""
    usfm: str
    human: str
    canonical: bool = True
    toc: bool = True


@dataclass
class ChapterContent:
    """Chapter content with verses."""
    id: int
    reference: str
    content: str
    verses: List[str]
    chapters: List[Chapter]
    version: Version


@dataclass
class Configuration:
    """Bible configuration."""
    versions: List[Version]
    languages: List[Language]
    stylesheets: Optional[List[dict]] = None


@dataclass
class RecommendedLanguages:
    """Recommended languages for a country."""
    languages: List[Language]
    country: str
