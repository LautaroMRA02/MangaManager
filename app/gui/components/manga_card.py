from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap


class MangaCard(QFrame):
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

        self.setObjectName("MangaCard")
        self.setFixedSize(180, 285)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("selected", False)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(7)

        # Portada
        self.cover_label = QLabel()
        self.cover_label.setObjectName("MangaCardCover")
        self.cover_label.setFixedSize(164, 210)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if cover and not cover.isNull():
            scaled = cover.scaled(
                self.cover_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.cover_label.setPixmap(scaled)
        else:
            self.cover_label.setText("Sin portada")

        layout.addWidget(
            self.cover_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Título principal
        self.title_label = QLabel(title)
        self.title_label.setObjectName("MangaCardTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setMaximumHeight(36)

        layout.addWidget(self.title_label)

        # Título original
        self.original_label = QLabel(original_title)
        self.original_label.setObjectName("MangaCardOriginal")
        self.original_label.setWordWrap(False)
        self.original_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )

        layout.addWidget(self.original_label)

        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.manga_id)

        super().mousePressEvent(event)
    def set_selected(self, selected):
        self.setProperty("selected", selected)

        self.style().unpolish(self)
        self.style().polish(self)

        self.update()