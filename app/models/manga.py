
from dataclasses import dataclass, field
from uuid import uuid4


def new_id():
    return str(uuid4())


@dataclass
class MangaTitle:
    language: str
    name: str
    original: bool = False

    def to_dict(self):
        return {
            "language": self.language,
            "name": self.name,
            "original": self.original
        }


@dataclass
class ChapterVersion:
    language: str
    id: str = field(default_factory=new_id)
    source_id: str = ""
    status: str = "pending"
    pages_total: int = 0
    pages_downloaded: int = 0
    folder: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "language": self.language,
            "source_id": self.source_id,
            "status": self.status,
            "pages_total": self.pages_total,
            "pages_downloaded": self.pages_downloaded,
            "folder": self.folder
        }


@dataclass
class Chapter:
    number: str
    id: str = field(default_factory=new_id)
    title: str = ""
    versions: list[ChapterVersion] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "versions": [
                version.to_dict() for version in self.versions
            ]
        }


@dataclass
class Manga:
    titles: list[MangaTitle]

    id: str = field(default_factory=new_id)
    description: str = ""
    cover: str | None = None
    status: str = "unknown"
    sources: list[dict] = field(default_factory=list)
    chapters: list[Chapter] = field(default_factory=list)

    @property
    def original_title(self):
        return next(
            (title for title in self.titles if title.original),
            None
        )

    def get_display_title(self, preferred_languages):
        for language in preferred_languages:
            for title in self.titles:
                if title.language.lower() == language.lower():
                    return title.name

        original = self.original_title

        if original:
            return original.name

        return self.titles[0].name if self.titles else "Unknown"

    def to_dict(self):
        return {
            "id": self.id,
            "titles": [title.to_dict() for title in self.titles],
            "description": self.description,
            "cover": self.cover,
            "status": self.status,
            "sources": self.sources,
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }

    @classmethod
    def from_dict(cls, data):
        # Migración desde la primera versión del modelo
        titles_data = data.get("titles")

        if not titles_data:
            old_title = data.get("title", "Unknown")
            titles_data = [{
                "language": "und",
                "name": old_title,
                "original": True
            }]

        chapters = []

        for item in data.get("chapters", []):
            versions_data = item.get("versions", [])

            # Compatibilidad con capítulos del modelo anterior
            if not versions_data and item.get("language"):
                versions_data = [{
                    "language": item["language"],
                    "status": item.get("status", "pending"),
                    "pages_total": item.get("pages_total", 0),
                    "pages_downloaded": item.get("pages_downloaded", 0),
                    "folder": item.get("folder", "")
                }]

            chapters.append(
                Chapter(
                    id=item.get("id", new_id()),
                    number=str(item.get("number", "")),
                    title=item.get("title", ""),
                    versions=[
                        ChapterVersion(**version)
                        for version in versions_data
                    ]
                )
            )

        return cls(
            id=data["id"],
            titles=[MangaTitle(**title) for title in titles_data],
            description=data.get("description", ""),
            cover=data.get("cover"),
            status=data.get("status", "unknown"),
            sources=data.get("sources", []),
            chapters=chapters
        )
