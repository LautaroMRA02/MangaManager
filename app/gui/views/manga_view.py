
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QGroupBox,
    QScrollArea,
    QSizePolicy,
    QListWidgetItem
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MangaView(QWidget):

    back_requested = Signal()
    add_chapter_requested = Signal()
    add_version_requested = Signal(str)

    delete_chapter_requested = Signal(str)
    delete_version_requested = Signal(str, str)

    edit_chapter_requested = Signal(str)
    edit_version_requested = Signal(str, str)

    
    def __init__(self):
        super().__init__()

        self.current_manga = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 25)
        main_layout.setSpacing(15)

        # Botón volver.
        back_button = QPushButton("< Volver a biblioteca")
        back_button.clicked.connect(self.back_requested.emit)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Área desplazable.
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setStyleSheet("""
            QScrollArea {
                background-color: #111318;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #111318;
            }
        """)

        self.scroll.viewport().setStyleSheet(
            "background-color: #111318;"
        )

        content = QWidget()
        content.setObjectName("MangaContent")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        content.setStyleSheet("""
            QWidget#MangaContent {
                background-color: #111318;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        # Información principal.
        info_layout = QHBoxLayout()
        info_layout.setSpacing(22)

        self.cover = QLabel()
        self.cover.setFixedSize(200, 280)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setStyleSheet("""
            QLabel {
                background-color: #20232D;
                border-radius: 8px;
                color: #9295A0;
            }
        """)

        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)

        self.title = QLabel("Manga")
        self.title.setObjectName("SectionTitle")
        self.title.setWordWrap(True)

        self.original_label = QLabel()
        self.original_label.setObjectName("Muted")
        self.original_label.setWordWrap(True)

        self.status_label = QLabel("Estado: Desconocido")
        self.status_label.setObjectName("Muted")

        description_title = QLabel("Descripción")
        description_title.setObjectName("SectionTitle")

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.description.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        details_layout.addWidget(self.title)
        details_layout.addWidget(self.original_label)
        details_layout.addWidget(self.status_label)
        details_layout.addWidget(description_title)
        details_layout.addWidget(self.description)
        details_layout.addStretch()

        info_layout.addWidget(self.cover)
        info_layout.addLayout(details_layout, 1)

        layout.addLayout(info_layout)

        # Títulos alternativos.
        titles_group = QGroupBox("Títulos e idiomas")
        titles_layout = QVBoxLayout(titles_group)
        self.titles_list = QListWidget()
        self.titles_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.titles_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.titles_list.setMaximumHeight(150)

        titles_layout.addWidget(self.titles_list)
        layout.addWidget(titles_group)

        # Capítulos.

        chapters_group = QGroupBox("Capítulos")
        chapters_layout = QVBoxLayout(chapters_group)
        chapters_layout.setSpacing(12)

        self.add_chapter_button = QPushButton("+ Agregar capítulo")
        self.add_chapter_button.setObjectName("Primary")
        self.add_chapter_button.clicked.connect(
            self.add_chapter_requested.emit
        )

        chapters_layout.addWidget(self.add_chapter_button)

        self.chapters_container = QWidget()
        self.chapters_container_layout = QVBoxLayout(
            self.chapters_container
        )
        self.chapters_container_layout.setContentsMargins(0, 0, 0, 0)
        self.chapters_container_layout.setSpacing(10)

        chapters_layout.addWidget(self.chapters_container)

        layout.addWidget(chapters_group)


        # self.chapters_list = QListWidget()
        # self.chapters_list.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        # self.chapters_list.setHorizontalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        # self.chapters_list.setMinimumHeight(220)

        # chapters_layout.addWidget(self.chapters_list)
        # layout.addWidget(chapters_group)

        self.scroll.setWidget(content)
        main_layout.addWidget(self.scroll)

    # --------------------------------------------------
    # Portada predeterminada
    # --------------------------------------------------

    def _default_cover(self):
        pixmap = QPixmap(300, 420)
        pixmap.fill(QColor("#20232D"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QColor("#7656E8"))
        painter.drawRoundedRect(15, 15, 270, 390, 15, 15)

        painter.setPen(QColor("#9295A0"))

        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(
            pixmap.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "MANGA"
        )

        painter.end()

        return pixmap

    def _load_cover(self, manga):
        pixmap = None

        if manga.cover:
            cover_path = Path(manga.cover)

            if not cover_path.is_absolute():
                cover_path = PROJECT_ROOT / cover_path

            if cover_path.is_file():
                loaded = QPixmap(str(cover_path))

                if not loaded.isNull():
                    pixmap = loaded

        if pixmap is None:
            pixmap = self._default_cover()

        self.cover.setPixmap(
            pixmap.scaled(
                QSize(200, 280),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    # --------------------------------------------------
    # Información del manga
    # --------------------------------------------------

    def _format_status(self, status):
        statuses = {
            "ongoing": "En publicación",
            "completed": "Finalizado",
            "hiatus": "En pausa",
            "cancelled": "Cancelado",
            "unknown": "Desconocido"
        }

        return statuses.get(status, status.capitalize())

    def _format_version_status(self, status):
        statuses = {
            "pending": "Pendiente",
            "downloading": "Descargando",
            "completed": "Completado",
            "error": "Error"
        }

        return statuses.get(status, status.capitalize())

    # --------------------------------------------------
    # Cargar manga
    # --------------------------------------------------

    def load_manga(self, manga, preferred_languages):
        self.current_manga = manga

        display_title = manga.get_display_title(
            preferred_languages
        )

        self.title.setText(display_title)

        original = manga.original_title

        if original:
            self.original_label.setText(
                f"Original: {original.name} · "
                f"Idioma: {original.language.upper()}"
            )
        else:
            self.original_label.setText(
                "Idioma original desconocido"
            )

        self.status_label.setText(
            f"Estado: {self._format_status(manga.status)}"
        )

        self.description.setText(
            manga.description or "Sin descripción disponible."
        )

        self._load_cover(manga)

        # Títulos alternativos.
        self.titles_list.clear()

        for title in manga.titles:
            marker = " ★ ORIGINAL" if title.original else ""

            self.titles_list.addItem(
                f"{title.language.upper()} · {title.name}{marker}"
            )

        # Mostrar capítulos agrupados con sus versiones.
        self.render_chapters(manga)


    def clear_chapters(self):
        while self.chapters_container_layout.count():
            item = self.chapters_container_layout.takeAt(0)

            widget = item.widget()
            if widget:
                widget.deleteLater()


    def render_chapters(self, manga):
        self.clear_chapters()

        if not manga.chapters:
            empty = QLabel("Todavía no hay capítulos registrados.")
            empty.setObjectName("Muted")
            self.chapters_container_layout.addWidget(empty)
            return

        for chapter in manga.chapters:
            chapter_card = QGroupBox(
                f"Capítulo {chapter.number} · {chapter.title or 'Sin título'}"
            )

            card_layout = QVBoxLayout(chapter_card)
            card_layout.setSpacing(8)

            # Versiones del capítulo.
            if chapter.versions:
                for version in chapter.versions:
                    status = self._format_version_status(version.status)
                    progress = (
                        f"{version.pages_downloaded}/"
                        f"{version.pages_total} páginas"
                    )

                    version_row = QHBoxLayout()

                    version_label = QLabel(
                        f"{version.language.upper()} · {progress}"
                    )

                    status_label = QLabel(status)
                    status_label.setObjectName("Muted")

                    edit_version_button = QPushButton("Editar")
                    edit_version_button.setObjectName("Secondary")
                    edit_version_button.clicked.connect(
                        lambda checked=False,
                        chapter_id=chapter.id,
                        version_id=version.id:
                        self.edit_version_requested.emit(
                            chapter_id, version_id
                        )
                    )

                    delete_version_button = QPushButton("Eliminar")
                    delete_version_button.setObjectName("Danger")
                    delete_version_button.clicked.connect(
                        lambda checked=False,
                        chapter_id=chapter.id,
                        version_id=version.id:
                        self.delete_version_requested.emit(
                            chapter_id, version_id
                        )
                    )

                    version_row.addWidget(version_label)
                    version_row.addStretch()
                    version_row.addWidget(status_label)
                    version_row.addWidget(edit_version_button)
                    version_row.addWidget(delete_version_button)

                    card_layout.addLayout(version_row)

            else:
                empty = QLabel("Todavía no hay versiones.")
                empty.setObjectName("Muted")
                card_layout.addWidget(empty)

            # Botones del capítulo.
            buttons_layout = QHBoxLayout()

            add_version_button = QPushButton("+ Agregar versión")
            add_version_button.setObjectName("Secondary")
            add_version_button.clicked.connect(
                lambda checked=False, chapter_id=chapter.id:
                self.add_version_requested.emit(chapter_id)
            )

            edit_chapter_button = QPushButton("Editar capítulo")
            edit_chapter_button.setObjectName("Secondary")
            edit_chapter_button.clicked.connect(
                lambda checked=False, chapter_id=chapter.id:
                self.edit_chapter_requested.emit(chapter_id)
            )

            delete_chapter_button = QPushButton("Eliminar capítulo")
            delete_chapter_button.setObjectName("Danger")
            delete_chapter_button.clicked.connect(
                lambda checked=False, chapter_id=chapter.id:
                self.delete_chapter_requested.emit(chapter_id)
            )

            buttons_layout.addWidget(add_version_button)
            buttons_layout.addStretch()
            buttons_layout.addWidget(edit_chapter_button)
            buttons_layout.addWidget(delete_chapter_button)

            card_layout.addLayout(buttons_layout)

            self.chapters_container_layout.addWidget(chapter_card)

        self.chapters_container_layout.addStretch()


