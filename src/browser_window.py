from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vanadium")
        self.resize(1280, 720)

        # Create the browser
        self.browser = QWebEngineView()

        # Load a webpage
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Make the browser fill the window
        self.setCentralWidget(self.browser)