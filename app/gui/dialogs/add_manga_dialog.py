
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AddMangaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Agregar manga")
        self.setMinimumWidth(430)
        self.setModal(True)

        # Fondo oscuro del diálogo.
        self.setStyleSheet("""
            QDialog {
                background-color: #111318;
                color: #E6E6E9;
            }
            QLabel {
                color: #E6E6E9;
            }
            QLabel#Muted {
                color: #9295A0;
            }
            QLineEdit, QComboBox {
                background-color: #1F222C;
                color: #E6E6E9;
                border: 1px solid #343844;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton {
                background-color: #292D38;
                color: #E6E6E9;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #383D4B;
            }
            QPushButton#Primary {
                background-color: #7656E8;
            }
            QPushButton#Primary:hover {
                background-color: #896CF0;
            }
        """)

        self.cover_path = None

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        title = QLabel("Agregar un nuevo manga")
        title.setObjectName("SectionTitle")

        description = QLabel(
            "Ingresá los datos principales del manga."
        )
        description.setObjectName("Muted")

        form = QFormLayout()
        form.setSpacing(12)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ej: 나 혼자만 레벨업")

        self.language_input = QComboBox()
        self.languages = [
            ("Español", "es"),
            ("English", "en"),
            ("Português (Brasil)", "pt-br"),
            ("日本語", "ja"),
            ("한국어", "ko"),
            ("中文", "zh"),
            ("Otro / Desconocido", "und")
        ]

        for name, code in self.languages:
            self.language_input.addItem(name, code)

        self.language_input.setCurrentIndex(4)

        form.addRow("Título original:", self.title_input)
        form.addRow("Idioma original:", self.language_input)

        # Selección de portada.
        cover_layout = QHBoxLayout()

        self.cover_preview = QLabel("Sin portada")
        self.cover_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_preview.setFixedSize(100, 140)
        self.cover_preview.setStyleSheet("""
            QLabel {
                background-color: #20232D;
                border: 1px dashed #555B6B;
                border-radius: 6px;
                color: #9295A0;
            }
        """)

        cover_buttons = QVBoxLayout()

        self.cover_button = QPushButton("Seleccionar imagen")
        self.cover_button.clicked.connect(self.select_cover)

        self.remove_cover_button = QPushButton("Quitar imagen")
        self.remove_cover_button.clicked.connect(self.remove_cover)
        self.remove_cover_button.setEnabled(False)

        cover_buttons.addWidget(self.cover_button)
        cover_buttons.addWidget(self.remove_cover_button)
        cover_buttons.addStretch()

        cover_layout.addWidget(self.cover_preview)
        cover_layout.addLayout(cover_buttons)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )
        save_button.setObjectName("Primary")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(form)
        layout.addWidget(QLabel("Portada"))
        layout.addLayout(cover_layout)
        layout.addStretch()
        layout.addWidget(buttons)

    def select_cover(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar portada",
            str(Path.home()),
            "Imágenes (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            return

        self.cover_path = file_path

        self.cover_preview.setPixmap(
            pixmap.scaled(
                self.cover_preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        self.remove_cover_button.setEnabled(True)

    def remove_cover(self):
        self.cover_path = None
        self.cover_preview.clear()
        self.cover_preview.setText("Sin portada")
        self.remove_cover_button.setEnabled(False)

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "language": self.language_input.currentData(),
            "cover": self.cover_path
        }

    def accept(self):
        if not self.title_input.text().strip():
            self.title_input.setFocus()
            self.title_input.setPlaceholderText(
                "El título no puede estar vacío"
            )
            return

        super().accept()
