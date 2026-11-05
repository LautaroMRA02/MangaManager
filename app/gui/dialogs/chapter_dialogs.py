
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QLabel
)


class AddChapterDialog(QDialog):
    def __init__(self, parent=None, chapter=None):
        super().__init__(parent)

        self.chapter = chapter
        editing = chapter is not None

        self.setWindowTitle(
            "Editar capítulo" if editing else "Agregar capítulo"
        )
        self.setMinimumWidth(380)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #111318;
                color: #E6E6E9;
            }
            QLabel {
                color: #E6E6E9;
            }
            QLineEdit {
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
        """)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Ej: 1, 2, 10.5")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ej: El comienzo")

        if editing:
            self.number_input.setText(str(chapter.number))
            self.title_input.setText(chapter.title)

        form.addRow("Número:", self.number_input)
        form.addRow("Título:", self.title_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.button(
            QDialogButtonBox.StandardButton.Save
        ).setObjectName("Primary")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(
            QLabel("Editar capítulo" if editing else "Nuevo capítulo")
        )
        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "number": self.number_input.text().strip(),
            "title": self.title_input.text().strip()
        }

    def accept(self):
        if not self.number_input.text().strip():
            self.number_input.setFocus()
            return

        super().accept()


class AddVersionDialog(QDialog):
    def __init__(
        self,
        languages,
        existing_languages=None,
        parent=None,
        current_language=None
    ):
        super().__init__(parent)

        editing = current_language is not None

        self.setWindowTitle(
            "Editar versión" if editing else "Agregar versión"
        )
        self.setMinimumWidth(380)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #111318;
                color: #E6E6E9;
            }
            QLabel {
                color: #E6E6E9;
            }
            QComboBox {
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
        """)

        existing = {
            language.lower()
            for language in (existing_languages or [])
        }

        if current_language:
            existing.discard(current_language.lower())

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.language_input = QComboBox()

        for language in languages:
            if language.lower() not in existing:
                self.language_input.addItem(
                    language.upper(),
                    language
                )

        if current_language:
            index = self.language_input.findData(current_language)
            if index >= 0:
                self.language_input.setCurrentIndex(index)

        form.addRow("Idioma de traducción:", self.language_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )
        save_button.setObjectName("Primary")
        save_button.setEnabled(self.language_input.count() > 0)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(
            QLabel("Editar versión" if editing else "Nueva versión")
        )
        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "language": self.language_input.currentData()
        }
