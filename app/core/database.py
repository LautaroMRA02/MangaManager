
import json
import os

from pathlib import Path
from tempfile import NamedTemporaryFile

from app.models.manga import Manga


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
LIBRARY_FILE = DATA_DIR / "library.json"


class LibraryDatabase:

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not LIBRARY_FILE.exists():
            self._save({"version": 2, "mangas": []})

    def _load(self):
        with LIBRARY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Formato de biblioteca inválido")

        if not isinstance(data.get("mangas"), list):
            raise ValueError("La lista de mangas no es válida")

        return data

    def _save(self, data):
        temp_path = None

        try:
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=DATA_DIR,
                suffix=".tmp",
                delete=False
            ) as file:
                temp_path = Path(file.name)

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, LIBRARY_FILE)

        except Exception:
            if temp_path and temp_path.exists():
                temp_path.unlink()
            raise

    def get_all(self):
        return [
            Manga.from_dict(item)
            for item in self._load()["mangas"]
        ]

    def get_by_id(self, manga_id):
        for item in self._load()["mangas"]:
            if item["id"] == manga_id:
                return Manga.from_dict(item)

        return None

    def add_manga(self, manga):
        data = self._load()

        if any(item["id"] == manga.id for item in data["mangas"]):
            raise ValueError("El manga ya está registrado")

        data["mangas"].append(manga.to_dict())
        data["version"] = 2
        self._save(data)

    def update_manga(self, manga):
        data = self._load()

        for index, item in enumerate(data["mangas"]):
            if item["id"] == manga.id:
                data["mangas"][index] = manga.to_dict()
                data["version"] = 2
                self._save(data)
                return True

        return False

    def remove_manga(self, manga_id):
        data = self._load()

        original_count = len(data["mangas"])

        data["mangas"] = [
            item for item in data["mangas"]
            if item["id"] != manga_id
        ]

        if len(data["mangas"]) == original_count:
            return False

        self._save(data)
        return True
