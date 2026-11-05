from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QStackedWidget,
    QInputDialog, QMessageBox, QFrame
)   
import shutil
from pathlib import Path

from PySide6.QtWidgets import QDialog

from app.core.database import LibraryDatabase
from app.core.config import AppConfig
from app.models.manga import (
    Manga,
    MangaTitle,
    Chapter,
    ChapterVersion
)
from app.gui.dialogs.chapter_dialogs import (
    AddChapterDialog,
    AddVersionDialog
)
from app.gui.styles import APP_STYLE
from app.gui.views.library_view import LibraryView
from app.gui.views.manga_view import MangaView
from app.gui.views.downloads_view import DownloadsView
from app.gui.views.editor_view import EditorView
from app.gui.views.settings_view import SettingsView
from app.gui.views.source_search_view import SourceSearchView

from app.gui.dialogs.add_manga_dialog import AddMangaDialog

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.database = LibraryDatabase()
        self.config = AppConfig()

        self.setWindowTitle("Manga Manager")
        self.resize(1100, 750)
        self.setMinimumSize(850, 600)
        self.setStyleSheet(APP_STYLE)

        self.setup_ui()
        self.refresh_library()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 16)
        sidebar_layout.setSpacing(6)



        app_title = QPushButton("Manga Manager")
        app_title.setObjectName("AppTitle")
        app_title.setEnabled(False)
        app_title.setFlat(True)

        sidebar_layout.addWidget(app_title)

        self.pages = QStackedWidget()

        self.library_view = LibraryView()
        self.manga_view = MangaView()
        self.downloads_view = DownloadsView()
        self.editor_view = EditorView()
        self.settings_view = SettingsView(self.config)
        self.source_search_view = SourceSearchView()

        self.pages.addWidget(self.library_view)
        self.pages.addWidget(self.manga_view)
        self.pages.addWidget(self.downloads_view)
        self.pages.addWidget(self.editor_view)
        self.pages.addWidget(self.settings_view)
        self.pages.addWidget(self.source_search_view)
        self.nav_buttons = []

        navigation = [
            ("Biblioteca", 0),
            ("Buscar en MangaDex", 5),
            ("Descargas", 2),
            ("Editor", 3),
        ]

        for label, page_index in navigation:
            button = QPushButton(label)
            button.setObjectName("SidebarButton")
            button.setCheckable(True)

            button.clicked.connect(
                lambda checked=False, index=page_index:
                self.navigate(index)
            )

            sidebar_layout.addWidget(button)
            self.nav_buttons.append((button, page_index))

        # Empuja Configuración hacia abajo
        # Empuja Configuración hacia abajo
        sidebar_layout.addStretch()

        # Separador visual
        separator = QFrame()
        separator.setObjectName("SidebarSeparator")
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(1)

        sidebar_layout.addWidget(separator)

        settings_button = QPushButton("Configuración")
        settings_button.setObjectName("SidebarButton")
        settings_button.setCheckable(True)

        settings_button.clicked.connect(
            lambda checked=False: self.navigate(4)
        )

        sidebar_layout.addWidget(settings_button)
        self.nav_buttons.append((settings_button, 4))

        root.addWidget(sidebar)
        root.addWidget(self.pages, 1)

        # Connections
        self.library_view.add_requested.connect(self.add_manga)

        self.library_view.manga_selected.connect(
            self.open_manga
        )

        self.manga_view.back_requested.connect(
            lambda: self.navigate(0)
        )
        self.manga_view.add_chapter_requested.connect(
        self.add_chapter
        )

        self.manga_view.add_version_requested.connect(
            self.add_chapter_version
        )
        self.manga_view.delete_chapter_requested.connect(
            self.delete_chapter
        )

        self.manga_view.delete_version_requested.connect(
            self.delete_chapter_version
        )
        self.manga_view.edit_chapter_requested.connect(
            self.edit_chapter
        )

        self.manga_view.edit_version_requested.connect(
            self.edit_chapter_version
        )
        self.source_search_view.manga_selected.connect(
            self.import_mangadex_manga
        )
        self.navigate(0)

    def navigate(self, index):
        self.pages.setCurrentIndex(index)

        for button, page_index in self.nav_buttons:
            button.setChecked(page_index == index)

        if index == 0:
            self.refresh_library()

        if index == 4:
            self.settings_view.load()

    def refresh_library(self):
        try:
            mangas = self.database.get_all()

            languages = self.config.get_preferred_languages()

            self.library_view.load_mangas(
                mangas,
                languages
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def add_manga(self):
        dialog = AddMangaDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        manga = Manga(
            titles=[
                MangaTitle(
                    language=data["language"],
                    name=data["title"],
                    original=True
                )
            ]
        )

        try:
            # Guardar portada, si se seleccionó una.
            if data["cover"]:
                project_root = Path(__file__).resolve().parents[2]
                covers_dir = project_root / "library" / "covers"
                covers_dir.mkdir(parents=True, exist_ok=True)

                extension = Path(data["cover"]).suffix.lower()
                cover_destination = covers_dir / f"{manga.id}{extension}"

                shutil.copy2(data["cover"], cover_destination)

                # Ruta relativa para guardar en el JSON.
                manga.cover = str(
                    cover_destination.relative_to(project_root)
                )

            self.database.add_manga(manga)
            self.refresh_library()

        except (ValueError, OSError) as error:
            QMessageBox.warning(
                self,
                "No se pudo agregar",
                str(error)
            )


    def import_mangadex_manga(self, result):
        # Comprobar si ya existe
        for existing in self.database.get_all():
            for source in existing.sources:
                if (
                    source.get("name") == "MangaDex"
                    and source.get("id") == result.source_id
                ):
                    QMessageBox.information(
                        self,
                        "Manga existente",
                        "Este manga ya está en tu biblioteca.",
                    )
                    return

        cover_path = None

        try:
            # Descargar portada
            if result.cover_url:
                project_root = Path(__file__).resolve().parents[2]
                covers_dir = project_root / "library" / "covers"
                covers_dir.mkdir(parents=True, exist_ok=True)

                cover_file = f"{result.source_id}.jpg"
                cover_absolute = covers_dir / cover_file

                response = self.scraper_download_cover(result.cover_url)

                with open(cover_absolute, "wb") as file:
                    file.write(response)

                cover_path = f"library/covers/{cover_file}"

            # Crear manga
            manga = Manga(
                titles=[
                    MangaTitle(
                        language=item["language"],
                        name=item["name"],
                        original=item["original"],
                    )
                    for item in result.titles
                ],
                sources=[
                    {
                        "id": result.source_id,
                        "name": "MangaDex",
                        "url": result.url,
                    }
                ],
                description=result.description,
                cover=cover_path,
            )

            self.database.add_manga(manga)
            self.library_view.render()

            QMessageBox.information(
                self,
                "Importación",
                f"{result.title} agregado a la biblioteca.",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo importar el manga:\n{error}",
            )


    def scraper_download_cover(self, url):
        response = self.source_search_view.scraper.session.get(
            url,
            timeout=20,
        )
        response.raise_for_status()

        return response.content


    def open_manga(self, manga_id):
        try:
            manga = self.database.get_by_id(manga_id)

            if manga is None:
                raise ValueError("No se encontró el manga.")

            languages = self.config.get_preferred_languages()
            self.current_manga_id = manga.id
            self.manga_view.load_manga(
                manga,
                languages
            )

            self.pages.setCurrentWidget(self.manga_view)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def add_chapter(self):
        manga = self.manga_view.current_manga

        if manga is None:
            return

        dialog = AddChapterDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        # Evitar números de capítulo duplicados.
        if any(
            chapter.number == data["number"]
            for chapter in manga.chapters
        ):
            QMessageBox.warning(
                self,
                "Capítulo duplicado",
                "Ya existe un capítulo con ese número."
            )
            return

        chapter = Chapter(
            number=data["number"],
            title=data["title"]
        )

        manga.chapters.append(chapter)

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            manga.chapters.remove(chapter)

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def edit_chapter(self, chapter_id):
        manga = self.database.get_by_id(self.current_manga_id)

        if manga is None:
            return

        chapter = next(
            (ch for ch in manga.chapters if ch.id == chapter_id),
            None
        )

        if chapter is None:
            return

        dialog = AddChapterDialog(self, chapter)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        # Evitar números duplicados en otros capítulos.
        if any(
            ch.id != chapter.id and ch.number == data["number"]
            for ch in manga.chapters
        ):
            QMessageBox.warning(
                self,
                "Capítulo duplicado",
                "Ya existe otro capítulo con ese número."
            )
            return

        old_number = chapter.number
        old_title = chapter.title

        chapter.number = data["number"]
        chapter.title = data["title"]

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            chapter.number = old_number
            chapter.title = old_title

            QMessageBox.critical(self, "Error", str(error))

    def add_chapter_version(self, chapter_id):
        manga = self.manga_view.current_manga

        if manga is None:
            return

        chapter = next(
            (item for item in manga.chapters if item.id == chapter_id),
            None
        )

        if chapter is None:
            QMessageBox.warning(self, "Error", "No se encontró el capítulo.")
            return

        preferred = self.config.get_preferred_languages()

        available_languages = list(dict.fromkeys(
            preferred + [title.language for title in manga.titles]
        ))

        existing_languages = [
            version.language for version in chapter.versions
        ]

        dialog = AddVersionDialog(
            available_languages,
            existing_languages,
            self
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        version = ChapterVersion(language=data["language"])

        chapter.versions.append(version)

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            chapter.versions.remove(version)
            QMessageBox.critical(self, "Error", str(error))

    def edit_chapter_version(self, chapter_id, version_id):
        manga = self.database.get_by_id(self.current_manga_id)

        if manga is None:
            return

        chapter = next(
            (ch for ch in manga.chapters if ch.id == chapter_id),
            None
        )

        if chapter is None:
            return

        version = next(
            (v for v in chapter.versions if v.id == version_id),
            None
        )

        if version is None:
            return

        preferred = self.config.get_preferred_languages()

        available_languages = list(dict.fromkeys(
            preferred + [title.language for title in manga.titles]
        ))

        existing_languages = [
            v.language
            for v in chapter.versions
        ]

        dialog = AddVersionDialog(
            available_languages,
            existing_languages,
            self,
            current_language=version.language
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()
        new_language = data["language"]

        if not new_language:
            return

        old_language = version.language
        version.language = new_language

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            version.language = old_language

            QMessageBox.critical(self, "Error", str(error))

    def reload_current_manga(self):
        manga = self.database.get_by_id(self.current_manga_id)
        
        if manga is None:
            raise ValueError("No se encontró el manga.")

        languages = self.config.get_preferred_languages()
        
        self.manga_view.load_manga(manga, languages)

    def delete_chapter(self, chapter_id):
        manga = self.database.get_by_id(self.current_manga_id)

        if not manga:
            return

        chapter = next(
            (ch for ch in manga.chapters if ch.id == chapter_id),
            None
        )

        if not chapter:
            return

        reply = QMessageBox.question(
            self,
            "Eliminar capítulo",
            (
                f"¿Estás seguro de que querés eliminar "
                f"el capítulo {chapter.number}?\n\n"
                "También se eliminarán todas sus versiones."
            ),
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        manga.chapters.remove(chapter)

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    def delete_chapter_version(self, chapter_id, version_id):
        manga = self.database.get_by_id(self.current_manga_id)

        if not manga:
            return

        chapter = next(
            (ch for ch in manga.chapters if ch.id == chapter_id),
            None
        )

        if not chapter:
            return

        version = next(
            (v for v in chapter.versions if v.id == version_id),
            None
        )

        if not version:
            return

        reply = QMessageBox.question(
            self,
            "Eliminar versión",
            (
                f"¿Estás seguro de que querés eliminar "
                f"la versión {version.language.upper()} "
                f"del capítulo {chapter.number}?"
            ),
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        chapter.versions.remove(version)

        try:
            self.database.update_manga(manga)
            self.reload_current_manga()

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))


