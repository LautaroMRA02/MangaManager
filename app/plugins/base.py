
from abc import ABC, abstractmethod
from dataclasses import dataclass,  field



@dataclass
class MangaSearchResult:
    source_id: str
    title: str
    url: str = ""
    cover_url: str = ""
    description: str = ""
    original_language: str = ""
    titles: list[dict] = field(default_factory=list)


@dataclass
class ChapterSearchResult:
    source_id: str
    number: str
    title: str = ""
    url: str = ""
    language: str = ""


@dataclass
class ChapterPage:
    number: int
    url: str


class BaseScraper(ABC):

    name = "Unknown"
    source_id = "unknown"

    @abstractmethod
    def search(self, query: str) -> list[MangaSearchResult]:
        """Busca mangas en la fuente."""
        pass

    @abstractmethod
    def get_chapters(
        self,
        manga_id: str
    ) -> list[ChapterSearchResult]:
        """Obtiene los capítulos de un manga."""
        pass

    @abstractmethod
    def get_pages(
        self,
        chapter_id: str
    ) -> list[ChapterPage]:
        """Obtiene las páginas de un capítulo."""
        pass
