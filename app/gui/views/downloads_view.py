
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DownloadsView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("Descargas")
        title.setObjectName("SectionTitle")

        description = QLabel(
            "Aquí administraremos las descargas, "
            "la cola de trabajos y el progreso."
        )
        description.setObjectName("Muted")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
