
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "data" / "settings.json"


DEFAULT_CONFIG = {
    "version": 1,
    "languages": {
        "preferred": ["es", "en", "pt-br"],
        "always_show_original": True
    },
    "downloads": {
        "max_workers": 4,
        "quality": "data"
    }
}


class AppConfig:

    def __init__(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not CONFIG_FILE.exists():
            self.save(DEFAULT_CONFIG)

    def load(self) -> dict:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, config: dict) -> None:
        temp_file = CONFIG_FILE.with_suffix(".tmp")

        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False
            )
            file.flush()

        temp_file.replace(CONFIG_FILE)

    def get_preferred_languages(self) -> list[str]:
        config = self.load()

        return config["languages"]["preferred"]
