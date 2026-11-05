
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QListView,
    QButtonGroup
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QPainter,
    QColor,
    QFont
)


from app.gui.components.manga_card import MangaCard

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class LibraryView(QWidget):
    manga_selected = Signal(str)
    add_requested = Signal()

    def __init__(self):
        super().__init__()

        self.mangas = []
        self.preferred_languages = []
        self.view_mode = "list"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Encabezado.
        header = QHBoxLayout()

        title = QLabel("biblioteca")
        title.setObjectName("SectionTitle")

        header.addWidget(title)
        header.addStretch()

        # Selector de visualización.
        self.list_button = QPushButton("Lista")
        self.grid_button = QPushButton("Cuadrícula")

        self.list_button.setCheckable(True)
        self.grid_button.setCheckable(True)
        self.list_button.setChecked(True)

        self.view_group = QButtonGroup(self)
        self.view_group.setExclusive(True)
        self.view_group.addButton(self.list_button)
        self.view_group.addButton(self.grid_button)

        self.list_button.clicked.connect(
            lambda: self.set_view_mode("list")
        )
        self.grid_button.clicked.connect(
            lambda: self.set_view_mode("grid")
        )

        header.addWidget(self.list_button)
        header.addWidget(self.grid_button)

        add_button = QPushButton("+ Agregar manga")
        add_button.setObjectName("Primary")
        add_button.clicked.connect(self.add_requested.emit)

        header.addWidget(add_button)

        # Búsqueda.
        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar por nombre...")
        self.search.textChanged.connect(self.render)

        # Biblioteca.
        self.list = QListWidget()
        self.list.setObjectName("LibraryList")
        self.list.setViewMode(QListView.ViewMode.ListMode)
        self.list.setUniformItemSizes(True)

        self.list.itemClicked.connect(self._on_item_clicked)

        layout.addLayout(header)
        layout.addWidget(self.search)
        layout.addWidget(self.list)

        self.set_view_mode("list")

    def _on_item_clicked(self, item):
        manga_id = item.data(Qt.ItemDataRole.UserRole)
        self.manga_selected.emit(manga_id)

    def load_mangas(self, mangas, preferred_languages):
        self.mangas = mangas
        self.preferred_languages = preferred_languages
        self.render()
    def set_view_mode(self, mode):
        self.view_mode = mode

        is_grid = mode == "grid"

        self.list_button.setChecked(not is_grid)
        self.grid_button.setChecked(is_grid)

        if is_grid:
            # Cuadrícula
            self.list.setViewMode(QListView.ViewMode.IconMode)
            self.list.setFlow(QListView.Flow.LeftToRight)
            self.list.setWrapping(True)
            self.list.setResizeMode(QListView.ResizeMode.Adjust)
            self.list.setMovement(QListView.Movement.Static)

            self.list.setIconSize(QSize(150, 210))
            self.list.setGridSize(QSize(190, 300))
            self.list.setSpacing(14)
            self.list.setWordWrap(True)

            self.list.setTextElideMode(Qt.TextElideMode.ElideRight)
            self.list.setItemAlignment(Qt.AlignmentFlag.AlignHCenter)

        else:
            # Lista
            self.list.setViewMode(QListView.ViewMode.ListMode)
            self.list.setFlow(QListView.Flow.TopToBottom)
            self.list.setWrapping(False)
            self.list.setResizeMode(QListView.ResizeMode.Fixed)
            self.list.setMovement(QListView.Movement.Static)

            self.list.setIconSize(QSize(0, 0))
            self.list.setGridSize(QSize())
            self.list.setSpacing(6)

            self.list.setWordWrap(False)
            self.list.setTextElideMode(Qt.TextElideMode.ElideRight)
            self.list.setItemAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.render()
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

    def _get_cover(self, manga):
        if manga.cover:
            cover_path = Path(manga.cover)

            if not cover_path.is_absolute():
                cover_path = PROJECT_ROOT / cover_path

            if cover_path.is_file():
                pixmap = QPixmap(str(cover_path))

                if not pixmap.isNull():
                    return pixmap

        return self._default_cover()

    def _scaled_cover(self, manga):
        cover = self._get_cover(manga)

        return cover.scaled(
            QSize(150, 210),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )


    def render(self):
        self.list.clear()

        query = self.search.text().strip().lower()

        for manga in self.mangas:
            title = manga.get_display_title(
                self.preferred_languages
            )

            all_titles = " ".join(
                item.name for item in manga.titles
            ).lower()

            if query and query not in all_titles:
                continue

            original = manga.original_title
            original_name = original.name if original else ""

            if self.view_mode == "grid":
                # Crear elemento contenedor
                item = QListWidgetItem()
                item.setData(
                    Qt.ItemDataRole.UserRole,
                    manga.id
                )
                item.setSizeHint(QSize(180, 280))

                self.list.addItem(item)

                # Crear tarjeta personalizada
                cover = self._get_cover(manga)

                card = MangaCard(
                    manga_id=manga.id,
                    title=title,
                    original_title=original_name,
                    cover=cover
                )

                card.clicked.connect(
                    self.manga_selected.emit
                )

                self.list.setItemWidget(item, card)

            else:
                # Vista de lista tradicional
                text = title

                if original_name and original_name != title:
                    text += f"  ·  Original: {original_name}"

                item = QListWidgetItem(text)

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    manga.id
                )

                item.setSizeHint(QSize(0, 40))
                item.setToolTip(title)

                self.list.addItem(item)
