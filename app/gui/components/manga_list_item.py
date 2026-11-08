
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap


class MangaListItem(QFrame):
    clicked = Signal(str)

    def __init__(
        self,
        manga_id,
        title,
        original_title="",
        cover=None
    ):
        super().__init__()

        self.manga_id = manga_id

        self.setObjectName("MangaListItem")
        self.setFixedHeight(90)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("selected", False)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 12, 8)
        layout.setSpacing(14)

        # Portada pequeña
        self.cover_label = QLabel()
        self.cover_label.setObjectName("MangaListCover")
        self.cover_label.setFixedSize(52, 72)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if cover and not cover.isNull():
            scaled = cover.scaled(
                self.cover_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.cover_label.setPixmap(scaled)
        else:
            self.cover_label.setText("N/A")

        layout.addWidget(self.cover_label)

        # Información
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("MangaListTitle")

        info_layout.addWidget(self.title_label)

        self.original_label = QLabel(original_title)
        self.original_label.setObjectName("MangaListOriginal")

        info_layout.addWidget(self.original_label)
        info_layout.addStretch()

        layout.addLayout(info_layout, 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.manga_id)

        super().mousePressEvent(event)
    def set_selected(self, selected):
        self.setProperty("selected", selected)

        self.style().unpolish(self)
        self.style().polish(self)

        self.update()