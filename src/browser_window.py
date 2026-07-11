from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import( QMainWindow, QToolBar, QLineEdit, QPushButton, QProgressBar,)
from PyQt6.QtWebEngineWidgets import QWebEngineView


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_browser()
        self.create_toolbar()
        self.create_progress_bar()
        self.connect_signals()


    def setup_window(self):
        """Configure the main application window."""
        self.setWindowTitle("Vanadium")
        self.resize(1280, 720)
        self.statusBar().showMessage("Ready")

    def create_browser(self):
        """Create and configure the browser widget."""
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://duckduckgo.com"))
        self.setCentralWidget(self.browser)

    def create_toolbar(self):
         """Create the navigation toolbar."""

         self.toolbar = QToolBar()
         self.addToolBar(self.toolbar)

    # Navigation buttons
         self.back_button = QPushButton("←")
         self.forward_button = QPushButton("→")
         self.reload_button = QPushButton("↻")
         self.home_button = QPushButton("🏠")

    # Address bar
         self.address_bar = QLineEdit()
         self.address_bar.setPlaceholderText("Search or enter address")

    # Go button
         self.go_button = QPushButton("Go")

    # Add widgets to toolbar
         self.toolbar.addWidget(self.back_button)
         self.toolbar.addWidget(self.forward_button)
         self.toolbar.addWidget(self.reload_button)
         self.toolbar.addWidget(self.home_button)
         self.toolbar.addWidget(self.address_bar)
         self.toolbar.addWidget(self.go_button)

    def connect_signals(self):
         """Connect buttons and widgets to their actions."""

         self.back_button.clicked.connect(self.browser.back)
         self.forward_button.clicked.connect(self.browser.forward)
         self.reload_button.clicked.connect(self.browser.reload)
         self.home_button.clicked.connect(self.go_home)

         self.go_button.clicked.connect(self.navigate)

         self.address_bar.returnPressed.connect(self.navigate)

         self.browser.urlChanged.connect(self.update_address_bar)
         self.browser.loadStarted.connect(self.load_started)
         self.browser.loadProgress.connect(self.update_progress)
         self.browser.loadFinished.connect(self.load_finished)
         self.browser.titleChanged.connect(self.update_window_title)

    def go_home(self):
         """Navigate to the homepage."""
         self.browser.setUrl(QUrl("https://duckduckgo.com"))

    def navigate(self):
         """Navigate to a website or search the web."""

         text = self.address_bar.text().strip()

         if not text:
             return

    # If it looks like a website
         if "." in text:
             if not text.startswith(("http://", "https://")):
                 text = "https://" + text

             url = QUrl(text)

    # Otherwise, search using DuckDuckGo
         else:
             search_url = f"https://duckduckgo.com/?q={text.replace(' ', '+')}"
             url = QUrl(search_url)

         self.browser.setUrl(url)

    def update_address_bar(self, url):
         """Update the address bar when the page changes."""

         self.address_bar.setText(url.toString())

    def create_progress_bar(self):
         """Create the page loading progress bar."""

         self.progress_bar = QProgressBar()

         self.progress_bar.setMaximumWidth(150)

         self.progress_bar.setVisible(False)

         self.statusBar().addPermanentWidget(self.progress_bar)

    def load_started(self):
         self.progress_bar.setVisible(True)
         self.statusBar().showMessage("Loading...")

    def update_progress(self, progress):
         """Update the loading progress."""

         self.progress_bar.setValue(progress)

    def load_finished(self):
         self.progress_bar.setVisible(False)
         self.statusBar().showMessage("Ready")

    def update_window_title(self, title):
         """Update the application window title."""

         self.setWindowTitle(f"{title} - Vanadium")