
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox,
    QMessageBox
)


class SettingsView(QWidget):

    def __init__(self, config):
        super().__init__()

        self.config = config

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Configuración")
        title.setObjectName("SectionTitle")

        languages_label = QLabel(
            "Idiomas preferidos (separados por coma)"
        )

        self.languages = QLineEdit()

        self.original_checkbox = QCheckBox(
            "Mostrar siempre el título original"
        )

        save_button = QPushButton("Guardar configuración")
        save_button.setObjectName("Primary")
        save_button.clicked.connect(self.save)

        layout.addWidget(title)
        layout.addWidget(languages_label)
        layout.addWidget(self.languages)
        layout.addWidget(self.original_checkbox)
        layout.addWidget(save_button)
        layout.addStretch()

        self.load()

    def load(self):
        data = self.config.load()
        languages = data["languages"]

        self.languages.setText(
            ", ".join(languages["preferred"])
        )

        self.original_checkbox.setChecked(
            languages.get("always_show_original", True)
        )

    def save(self):
        try:
            languages = [
                language.strip().lower()
                for language in self.languages.text().split(",")
                if language.strip()
            ]

            if not languages:
                raise ValueError("Ingresá al menos un idioma.")

            data = self.config.load()

            data["languages"]["preferred"] = list(
                dict.fromkeys(languages)
            )

            data["languages"]["always_show_original"] = (
                self.original_checkbox.isChecked()
            )

            self.config.save(data)

            QMessageBox.information(
                self,
                "Configuración",
                "Preferencias guardadas correctamente."
            )

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))
