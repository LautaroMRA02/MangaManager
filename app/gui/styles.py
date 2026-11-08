
APP_STYLE = """
/* ========================
   PALETA GENERAL
   ======================== */

QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    color: #cdd6f4;
    font-family: "Ubuntu";
    font-size: 13px;
}

/* ========================
   SIDEBAR
   ======================== */

QFrame#Sidebar {
    background-color: #181825;
    border: none;
}
QFrame#SidebarSeparator {
    background-color: #313244;
    border: none;
    max-height: 1px;
    margin-top: 8px;
    margin-bottom: 8px;
}

QPushButton#AppTitle {
    background-color: transparent;
    color: #cdd6f4;
    font-size: 20px;
    font-weight: bold;
    text-align: left;
    padding: 8px 6px;
    border: none;
}

QPushButton#SidebarButton {
    background-color: transparent;
    color: #a6adc8;
    text-align: left;
    padding: 11px 14px;
    border: none;
    border-radius: 8px;
    font-weight: 500;
}

QPushButton#SidebarButton:hover {
    background-color: #313244;
    color: #cdd6f4;
}

QPushButton#SidebarButton:checked {
    background-color: #45405f;
    color: #cba6f7;
    font-weight: bold;
}

/* ========================
   TITULOS
   ======================== */

QLabel#SectionTitle {
    font-size: 23px;
    font-weight: bold;
    color: #cdd6f4;
}

QLabel#Muted {
    color: #9399b2;
}

/* ========================
   BOTONES GENERALES
   ======================== */

QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-radius: 8px;
    padding: 9px 14px;
}

QPushButton:hover {
    background-color: #45475a;
}

QPushButton:pressed {
    background-color: #585b70;
}

QPushButton:disabled {
    background-color: #242438;
    color: #6c7086;
}

QPushButton#Primary {
    background-color: #cba6f7;
    color: #1e1e2e;
    font-weight: bold;
}

QPushButton#Primary:hover {
    background-color: #b4befe;
}

/* ========================
   CAMPOS DE TEXTO
   ======================== */

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 9px;
    selection-background-color: #585b70;
    selection-color: #ffffff;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus {
    border: 1px solid #cba6f7;
}

QComboBox QAbstractItemView {
    background-color: #181825;
    color: #cdd6f4;
    selection-background-color: #45405f;
    border: 1px solid #45475a;
}

/* ========================
   LISTAS
   ======================== */

QListWidget {
    background-color: #181825;
    border: none;
    border-radius: 8px;
    padding: 5px;
    outline: none;
}

QListWidget::item {
    padding: 10px;
    border-radius: 6px;
}

QListWidget::item:hover {
    background-color: #313244;
}

QListWidget::item:selected {
    background-color: #45405f;
    color: #cba6f7;
}

/* ========================
   PESTAÑAS Y SCROLL
   ======================== */

QTabWidget::pane {
    border: none;
}

QTabBar::tab {
    background-color: #181825;
    color: #a6adc8;
    padding: 9px 15px;
    border-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #45405f;
    color: #cba6f7;
}

QScrollArea {
    border: none;
    background: transparent;
}

/* ========================
   CHECKBOX
   ======================== */

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
}

/* ========================
   MENSAJES
   ======================== */

QMessageBox {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

QMessageBox QLabel {
    background-color: transparent;
    color: #cdd6f4;
    padding: 8px;
}

QMessageBox QDialogButtonBox {
    background-color: transparent;
    padding: 8px;
}

QMessageBox QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 9px 16px;
    min-width: 70px;
}

QMessageBox QPushButton:hover {
    background-color: #45475a;
}

QMessageBox QPushButton:default {
    border: 1px solid #cba6f7;
}
/* ========================
   BIBLIOTECA
   ======================== */

QListWidget#LibraryList {
    background-color: transparent;
    border: none;
    padding: 8px;
    outline: none;
}

QListWidget#LibraryList::item {
    padding: 0px;
    border: none;
    background: transparent;
}

QFrame#MangaCard {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
}

QFrame#MangaCard:hover {
    background-color: #242438;
    border: 1px solid #cba6f7;
}
QListWidget#LibraryList::item:hover {
    background-color: #313244;
}

QListWidget#LibraryList::item:selected {
    background-color: #45405f;
    color: #cba6f7;
}
/* ========================
   MANGA CARDS
   ======================== */

QFrame#MangaCard {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
}

QFrame#MangaCard:hover {
    background-color: #242438;
    border: 1px solid #cba6f7;
}

QLabel#MangaCardCover {
    border-radius: 6px;
    color: #9399b2;
}

QLabel#MangaCardTitle {
    color: #cdd6f4;
    font-size: 13px;
    font-weight: bold;
    background: transparent;
    
}

QLabel#MangaCardOriginal {
    color: #9399b2;
    font-size: 11px;
    background: transparent;
}

/* ========================
   MANGA LIST ITEMS
   ======================== */

QFrame#MangaListItem {
    background-color: #181825;
    border: 1px solid transparent;
    border-radius: 9px;
}

QFrame#MangaListItem:hover {
    background-color: #242438;
    border: 1px solid #cba6f7;
}

QLabel#MangaListCover {
    background-color: #313244;
    border-radius: 5px;
    color: #9399b2;
}

QLabel#MangaListTitle {
    color: #cdd6f4;
    font-size: 14px;
    font-weight: bold;
    background: transparent;
}

QLabel#MangaListOriginal {
    color: #9399b2;
    font-size: 11px;
    background: transparent;
}
/* ========================
   LIBRARY HEADER
   ======================== */

QLineEdit#LibrarySearch {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 9px 12px;
}

QLineEdit#LibrarySearch:focus {
    border: 1px solid #cba6f7;
}

QPushButton#ViewModeButton {
    background-color: #181825;
    color: #a6adc8;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 9px 12px;
}

QPushButton#ViewModeButton:hover {
    background-color: #313244;
}

QPushButton#ViewModeButton:checked {
    background-color: #45405f;
    color: #cba6f7;
    border: 1px solid #585b70;
}
/* ========================
   SELECCION DE MANGAS
   ======================== */

QFrame#MangaCard[selected="true"] {
    background-color: #242438;
    border: 1px solid #cba6f7;
}

QFrame#MangaListItem[selected="true"] {
    background-color: #242438;
    border: 1px solid #cba6f7;
}
/* =========================
   MangaView
========================= */

QLabel#MangaCover {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
    color: #9399b2;
}

QGroupBox#MangaSection {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
    margin-top: 14px;
    padding: 12px;
    font-weight: bold;
}

QGroupBox#MangaSection::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #cba6f7;
}

QFrame#ChapterCard {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 9px;
}

QFrame#ChapterCard:hover {
    border: 1px solid #45405f;
}

QLabel#ChapterTitle {
    color: #cdd6f4;
    font-size: 14px;
    font-weight: bold;
    background: transparent;
}

QLabel#VersionLabel {
    color: #cdd6f4;
    background: transparent;
}

QLabel#VersionStatus {
    color: #a6adc8;
    background: transparent;
}

QPushButton#Secondary {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid transparent;
    border-radius: 7px;
    padding: 7px 10px;
}

QPushButton#Secondary:hover {
    background-color: #45405f;
    border: 1px solid #585b70;
}

QPushButton#Danger {
    background-color: #313244;
    color: #f38ba8;
    border: 1px solid transparent;
    border-radius: 7px;
    padding: 7px 10px;
}

QPushButton#Danger:hover {
    background-color: #49283a;
    border: 1px solid #f38ba8;
}
QPushButton#BackButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45405f;
    border-radius: 8px;
    padding: 7px 12px;
    font-weight: bold;
}

QPushButton#BackButton:hover {
    background-color: #45405f;
    border: 1px solid #cba6f7;
    color: #cba6f7;
}

QPushButton#BackButton:pressed {
    background-color: #585b70;
}
QListWidget#MangaTitlesList {
    background: transparent;
    border: none;
    padding: 2px;
    outline: none;
}

QListWidget#MangaTitlesList::item {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-radius: 5px;
    padding: 5px 8px;
    margin: 1px 0;
}

QListWidget#MangaTitlesList::item:hover {
    background-color: #313244;
}

QListWidget#MangaTitlesList::item:selected {
    background-color: #45405f;
    color: #cba6f7;
}
QFrame#ChapterSeparator {
    background-color: #313244;
    border: none;
    max-height: 1px;
}
/* Estados de versiones */

QLabel#VersionStatus[status="pending"] {
    color: #f9e2af;
    background-color: #45405f;
    border-radius: 6px;
    padding: 4px 8px;
}

QLabel#VersionStatus[status="downloading"] {
    color: #89dceb;
    background-color: #263b4d;
    border-radius: 6px;
    padding: 4px 8px;
}

QLabel#VersionStatus[status="completed"] {
    color: #a6e3a1;
    background-color: #263b35;
    border-radius: 6px;
    padding: 4px 8px;
}

QLabel#VersionStatus[status="error"] {
    color: #f38ba8;
    background-color: #49283a;
    border-radius: 6px;
    padding: 4px 8px;
}
/* Scroll de MangaView */

QScrollBar:vertical {
    background-color: #181825;
    width: 10px;
    border: none;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #45405f;
    border-radius: 5px;
    min-height: 35px;
}

QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QLabel#MangaDetailTitle {
    color: #CDD6F4;
    font-size: 25px;
    font-weight: bold;
}

QLabel#MangaStatus {
    background-color: #313244;
    color: #CBA6F7;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 5px 10px;
    max-width:200px;
}

"""
