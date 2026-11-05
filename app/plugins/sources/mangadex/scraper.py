
import requests

from app.plugins.base import (
    BaseScraper,
    MangaSearchResult,
    ChapterSearchResult,
    ChapterPage,
)


class MangaDexScraper(BaseScraper):

    name = "MangaDex"
    source_id = "mangadex"

    BASE_URL = "https://api.mangadex.org"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MangaManager/1.0"
        })

    def search(self, query: str) -> list[MangaSearchResult]:
        response = self.session.get(
            f"{self.BASE_URL}/manga",
            params={
                "title": query,
                "limit": 10,
                "includes[]": ["cover_art"],
            },
            timeout=15,
        )
        response.raise_for_status()

        results = []

        for manga in response.json()["data"]:
            attributes = manga["attributes"]


            titles = attributes.get("title", {})
            original_language = attributes.get("originalLanguage", "")

            title = (
                titles.get("es")
                or titles.get("en")
                or next(iter(titles.values()), "Sin título")
            )

            manga_titles = []

            # Títulos principales
            for language, name in titles.items():
                manga_titles.append({
                    "language": language,
                    "name": name,
                    "original": language == original_language,
                })

            # Títulos alternativos
            for alternative in attributes.get("altTitles", []):
                for language, name in alternative.items():
                    if not any(
                        item["language"] == language
                        and item["name"] == name
                        for item in manga_titles
                    ):
                        manga_titles.append({
                            "language": language,
                            "name": name,
                            "original": False,
                        })

            cover_url = ""

            for relationship in manga.get("relationships", []):
                if relationship["type"] == "cover_art":
                    filename = relationship["attributes"]["fileName"]
                    cover_url = (
                        f"https://uploads.mangadex.org/covers/"
                        f"{manga['id']}/{filename}.256.jpg"
                    )
                    break

            results.append(
                MangaSearchResult(
                    source_id=manga["id"],
                    title=title,
                    url=f"https://mangadex.org/title/{manga['id']}",
                    cover_url=cover_url,
                    description=attributes.get("description", {}).get("en", ""),
                    original_language=original_language,
                    titles=manga_titles,
                )
            )

        return results

    def get_chapters(
        self,
        manga_id: str
    ) -> list[ChapterSearchResult]:

        response = self.session.get(
            f"{self.BASE_URL}/manga/{manga_id}/feed",
            params={
                "limit": 100,
                "translatedLanguage[]": ["es"],
                "order[chapter]": "asc",
            },
            timeout=15,
        )
        response.raise_for_status()

        chapters = []

        for chapter in response.json()["data"]:
            attributes = chapter["attributes"]

            chapters.append(
                ChapterSearchResult(
                    source_id=chapter["id"],
                    number=attributes.get("chapter") or "0",
                    title=attributes.get("title") or "",
                    url=f"https://mangadex.org/chapter/{chapter['id']}",
                    language=attributes.get("translatedLanguage", ""),
                )
            )

        return chapters

    def get_pages(
        self,
        chapter_id: str
    ) -> list[ChapterPage]:

        response = self.session.get(
            f"{self.BASE_URL}/at-home/server/{chapter_id}",
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()

        base_url = data["baseUrl"]
        chapter = data["chapter"]
        chapter_hash = chapter["hash"]

        filenames = chapter["data"]

        pages = []

        for index, filename in enumerate(filenames, start=1):
            url = (
                f"{base_url}/data/"
                f"{chapter_hash}/{filename}"
            )

            pages.append(
                ChapterPage(
                    number=index,
                    url=url,
                )
            )

        return pages
