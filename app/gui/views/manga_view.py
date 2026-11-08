
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
    QListWidgetItem,
    QFrame
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
        main_layout.setContentsMargins(28, 22, 28, 28)
        main_layout.setSpacing(12)

        # Botón volver.
        back_button = QPushButton("←  Biblioteca")
        back_button.setObjectName("BackButton")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(self.back_requested.emit)
        back_button.setFixedHeight(36)
        back_button.setFixedWidth(150)
        main_layout.addWidget(
            back_button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        # Área desplazable.
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        self.scroll.viewport().setStyleSheet(
            "background: transparent;"
        )
        content = QWidget()
        content.setObjectName("MangaContent")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        content.setStyleSheet("""
            QWidget#MangaContent {
                background: transparent;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(22)

        # Información principal.

        # Información principal.

        # Información principal.
        info_layout = QHBoxLayout()
        info_layout.setSpacing(22)

        # Portada.
        self.cover = QLabel()
        self.cover.setObjectName("MangaCover")
        self.cover.setFixedSize(160, 225)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Información.
        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)

        self.title = QLabel("Manga")
        self.title.setObjectName("MangaDetailTitle")
        self.title.setWordWrap(True)

        self.original_label = QLabel()
        self.original_label.setObjectName("Muted")
        self.original_label.setWordWrap(True)

        self.status_label = QLabel("Estado: Desconocido")
        self.status_label.setObjectName("MangaStatus")
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        description_title = QLabel("Descripción")
        description_title.setObjectName("SectionTitle")

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setAlignment(
            Qt.AlignmentFlag.AlignTop |
            Qt.AlignmentFlag.AlignLeft
        )
        self.description.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        details_layout.addWidget(self.title)
        details_layout.addWidget(self.original_label)
        details_layout.addWidget(self.status_label)
        details_layout.addSpacing(6)
        details_layout.addWidget(description_title)
        details_layout.addWidget(self.description)
        details_layout.addStretch()

        info_layout.addWidget(self.cover)
        info_layout.addLayout(details_layout, 1)

        layout.addLayout(info_layout)




        # Títulos alternativos.
        titles_group = QGroupBox("Títulos e idiomas")
        titles_group.setObjectName("MangaSection")

        titles_layout = QVBoxLayout(titles_group)
        titles_layout.setContentsMargins(12, 12, 12, 12)
        titles_layout.setSpacing(4)

        self.titles_list = QListWidget()
        self.titles_list.setObjectName("MangaTitlesList")
        self.titles_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.titles_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.titles_list.setMinimumHeight(0)
        self.titles_list.setMaximumHeight(16777215)
        self.titles_list.setSpacing(4)
        self.titles_list.setUniformItemSizes(True)

        self.titles_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        titles_layout.addWidget(self.titles_list)
        layout.addWidget(titles_group)


        # Capítulos.

        chapters_group = QGroupBox("Capítulos")
        chapters_group.setObjectName("MangaSection")
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
        self.chapters_container_layout.setSpacing(12)

        chapters_layout.addWidget(self.chapters_container)

        layout.addWidget(chapters_group)

        self.scroll.setWidget(content)
        main_layout.addWidget(self.scroll)

    # --------------------------------------------------
    # Portada predeterminada
    # --------------------------------------------------

    def _default_cover(self):
        pixmap = QPixmap(300, 420)
        pixmap.fill(QColor("#181825"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QColor("#7656E8"))
        painter.drawRoundedRect(15, 15, 270, 390, 15, 15)

        painter.setPen(QColor("#cba6f7"))

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
                QSize(160, 225),
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
    def _adjust_titles_height(self):
        count = self.titles_list.count()

        if count == 0:
            self.titles_list.setFixedHeight(0)
            return
        row_height = self.titles_list.sizeHintForRow(0)

        if row_height <= 0:
            row_height = 30

        spacing = self.titles_list.spacing()
        margins = self.titles_list.contentsMargins()

        total_height = (
            count * row_height
            + max(0, count - 1) * spacing
            + margins.top()
            + margins.bottom()
            + 8
        )

        self.titles_list.setFixedHeight(total_height)
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
        self._adjust_titles_height()
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
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setMinimumHeight(60)
            self.chapters_container_layout.addWidget(empty)
            return

        for chapter in manga.chapters:
            # Tarjeta del capítulo.
            chapter_card = QFrame()
            chapter_card.setObjectName("ChapterCard")
            chapter_card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum
            )
            card_layout = QVBoxLayout(chapter_card)
            card_layout.setContentsMargins(16, 14, 16, 14)
            card_layout.setSpacing(12)

            # Encabezado.
            header = QHBoxLayout()

            chapter_title = QLabel(
                f"Capítulo {chapter.number} · "
                f"{chapter.title or 'Sin título'}"
            )
            chapter_title.setObjectName("ChapterTitle")
            chapter_title.setWordWrap(True)

            versions_count = QLabel(
                f"{len(chapter.versions)} versiones"
            )
            versions_count.setObjectName("Muted")

            header.addWidget(chapter_title, 1)
            header.addWidget(versions_count)

            card_layout.addLayout(header)

            # Versiones.
            if chapter.versions:
                for version in chapter.versions:
                    version_row = QHBoxLayout()
                    version_row.setSpacing(8)

                    version_label = QLabel(
                        f"{version.language.upper()} · "
                        f"{version.pages_downloaded}/"
                        f"{version.pages_total} páginas"
                    )
                    version_label.setObjectName("VersionLabel")

                    status_label = QLabel(
                        self._format_version_status(version.status)
                    )
                    status_label.setObjectName("VersionStatus")
                    status_label.setProperty("status", version.status)
                    status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    status_label.setMinimumWidth(95)

                    edit_version_button = QPushButton("Editar")
                    edit_version_button.setObjectName("Secondary")
                    edit_version_button.setFixedWidth(70)
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
                    delete_version_button.setFixedWidth(80)
                    delete_version_button.clicked.connect(
                        lambda checked=False,
                        chapter_id=chapter.id,
                        version_id=version.id:
                        self.delete_version_requested.emit(
                            chapter_id, version_id
                        )
                    )

                    version_row.addWidget(version_label, 1)
                    version_row.addWidget(status_label)
                    version_row.addWidget(edit_version_button)
                    version_row.addWidget(delete_version_button)

                    card_layout.addLayout(version_row)

            else:
                empty_versions = QLabel("Todavía no hay versiones.")
                empty_versions.setObjectName("Muted")
                card_layout.addWidget(empty_versions)

            # Separador.
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setObjectName("ChapterSeparator")
            card_layout.addWidget(separator)

   
            # Acciones de versiones.
            version_actions = QHBoxLayout()

            add_version_button = QPushButton("+ Agregar versión")
            add_version_button.setObjectName("Secondary")
            add_version_button.clicked.connect(
                lambda checked=False, chapter_id=chapter.id:
                self.add_version_requested.emit(chapter_id)
            )

            version_actions.addWidget(add_version_button)
            version_actions.addStretch()

            card_layout.addLayout(version_actions)

            # Acciones del capítulo.
            chapter_actions = QHBoxLayout()

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

            chapter_actions.addWidget(edit_chapter_button)
            chapter_actions.addWidget(delete_chapter_button)
            chapter_actions.addStretch()

            card_layout.addLayout(chapter_actions)


            self.chapters_container_layout.addWidget(chapter_card)

        self.chapters_container_layout.addStretch()

