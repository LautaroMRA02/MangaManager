
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
)

from app.plugins.sources.mangadex.scraper import MangaDexScraper


class SourceSearchView(QWidget):

    manga_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scraper = MangaDexScraper()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Buscador
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar manga en MangaDex...")

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_manga)

        self.search_input.returnPressed.connect(self.search_manga)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        # Resultados
        self.results_list = QListWidget()
        self.results_list.setIconSize(self.results_list.iconSize())
        self.results_list.itemDoubleClicked.connect(
            self.select_manga
        )

        layout.addWidget(self.results_list)

        # Seleccionar
        self.select_button = QPushButton("Seleccionar manga")
        self.select_button.clicked.connect(self.select_current)

        layout.addWidget(self.select_button)

    def search_manga(self):
        query = self.search_input.text().strip()

        if not query:
            return

        self.results_list.clear()
        self.search_button.setEnabled(False)
        self.search_button.setText("Buscando...")

        try:
            results = self.scraper.search(query)

            for manga in results:
                item = QListWidgetItem(manga.title)
                item.setData(Qt.ItemDataRole.UserRole, manga)

                self.results_list.addItem(item)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error de búsqueda",
                str(error),
            )

        finally:
            self.search_button.setEnabled(True)
            self.search_button.setText("Buscar")

    def select_current(self):
        item = self.results_list.currentItem()

        if item is None:
            return

        manga = item.data(Qt.ItemDataRole.UserRole)
        self.manga_selected.emit(manga)

    def select_manga(self, item):
        manga = item.data(Qt.ItemDataRole.UserRole)
        self.manga_selected.emit(manga)
