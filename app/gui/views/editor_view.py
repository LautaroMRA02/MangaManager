
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class EditorView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("Editor")
        title.setObjectName("SectionTitle")

        description = QLabel(
            "Espacio reservado para herramientas de edición, "
            "recorte y procesamiento de páginas."
        )
        description.setObjectName("Muted")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
