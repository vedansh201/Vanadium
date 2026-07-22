from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import( QMainWindow, QToolBar, QLineEdit, QPushButton, QProgressBar,)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from tab_widget import BrowserTabs
from PyQt6.QtGui import (QAction, QShortcut, QKeySequence)
from pathlib import Path
from settings_dialog import SettingsDialog
from settings_manager import load_settings
from bridge import BrowserBridge
from PyQt6.QtWebChannel import QWebChannel
from bookmark_manager import BookmarkManager
from PyQt6.QtWidgets import QMenu
from history_manager import HistoryManager
from history_dialog import HistoryDialog
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWidgets import QFileDialog
from download_manager import DownloadManager
from downloads_dialog import DownloadsDialog

class BrowserWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setup_window()

        self.bridge = BrowserBridge(self)
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.bookmarks = BookmarkManager()
        self.history = HistoryManager()
        self.download_manager = DownloadManager()
        self.active_downloads = []
        self.create_browser()
        self.create_toolbar()
        self.create_progress_bar()
        self.connect_signals()
        self.create_shortcuts()

        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button.clicked.connect(self.reload_page)
        self.refresh_bookmarks()
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

    def setup_window(self):
        """Configure the main application window."""
        self.setWindowTitle("Vanadium")
        self.resize(1280, 720)
        self.statusBar().showMessage("Ready")

    def create_browser(self):
        """Create and configure the browser widget."""
        self.tabs = BrowserTabs()
        self.setCentralWidget(self.tabs)
        self.tabs.create_tab(channel=self.channel)

    def create_toolbar(self):
         """Create the navigation toolbar."""

         self.toolbar = QToolBar()
         self.addToolBar(self.toolbar)

    # Navigation buttons
         self.back_button = QPushButton("←")
         self.forward_button = QPushButton("→")
         self.reload_button = QPushButton("↻")
         self.home_button = QPushButton("🏠")
         self.settings_button = QPushButton("⚙")
         self.bookmark_button = QPushButton("⭐")
         self.bookmarks_menu = QMenu("Bookmarks", self)
         self.history_button = QPushButton("📜")
         self.downloads_button = QPushButton("⬇")
         self.toolbar.addWidget(self.downloads_button)
         self.toolbar.addWidget(self.history_button)

         self.bookmarks_dropdown = QPushButton("▼")
         self.bookmarks_dropdown.setMenu(self.bookmarks_menu)

         self.toolbar.addWidget(self.bookmarks_dropdown)
         self.new_tab_button = QAction("New Tab", self)
         self.new_tab_button.setStatusTip("Open a new tab")
         self.toolbar.addAction(self.new_tab_button)

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
         self.toolbar.addWidget(self.settings_button)
         self.toolbar.addWidget(self.bookmark_button)
         self.toolbar.addWidget(self.address_bar)
         self.toolbar.addWidget(self.go_button)

    def connect_signals(self):
         """Connect buttons and widgets to their actions."""
                                                 
                                                 
         self.back_button.clicked.connect(self.tabs.current_browser().back)
         self.forward_button.clicked.connect(self.tabs.current_browser().forward)
         self.reload_button.clicked.connect(self.tabs.current_browser().reload)
         self.home_button.clicked.connect(self.go_home)
         self.settings_button.clicked.connect(self.open_settings)
         self.bookmark_button.clicked.connect(self.add_bookmark)
         self.history_button.clicked.connect(self.open_history)
         self.downloads_button.clicked.connect(
                self.open_downloads
          )
         self.go_button.clicked.connect(self.navigate)

         self.address_bar.returnPressed.connect(self.navigate)

         self.tabs.url_changed.connect(self.update_address_bar)
         self.tabs.load_started.connect(self.load_started)
         self.tabs.load_progress.connect(self.update_progress)
         self.tabs.load_finished.connect(self.load_finished)
         self.tabs.title_changed.connect(self.update_window_title)
         self.new_tab_button.triggered.connect(lambda: self.tabs.create_tab(channel=self.channel))
         self.tabs.add_tab_button.clicked.connect(
                lambda: self.tabs.create_tab(channel=self.channel)
          )

    def go_home(self):
           home = (Path(__file__).parent.parent / "assets" / "home" / "home.html").resolve()
           self.tabs.current_browser().setUrl(QUrl.fromLocalFile(str(home)))

    def navigate(self):
           self.navigate_to_text(self.address_bar.text())
           
    def update_address_bar(self, url):
         """Update the address bar when the page changes."""
         if url.scheme() == "vanadium":
                print(url.toString())
                return
         if url.isLocalFile():
                self.address_bar.setText("vanadium://home")
                return
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
         browser = self.tabs.current_browser()
         print("Page finished loading!")

         if browser:
                self.history.add_visit(
                     browser.title(),
                     browser.url().toString()
                )

    def update_window_title(self, title):
         """Update the application window title."""

         self.setWindowTitle(f"{title} - Vanadium")


    def go_back(self):
           browser = self.tabs.current_browser()
           if browser:
                browser.back()


    def go_forward(self):
           browser = self.tabs.current_browser()
           if browser:
                browser.forward()


    def reload_page(self):
           browser = self.tabs.current_browser()
           if browser:
                browser.reload()

    def create_shortcuts(self):
           """Create keyboard shortcuts."""

           self.new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
           self.new_tab_shortcut.activated.connect(
                lambda: self.tabs.create_tab(channel=self.channel)
          )
           self.close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
           self.close_tab_shortcut.activated.connect(self.close_current_tab)
           self.address_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
           self.address_shortcut.activated.connect(self.focus_address_bar)

    def close_current_tab(self):
           """Close the currently selected tab."""
   
           index = self.tabs.currentIndex()
           self.tabs.close_tab(index)

    def focus_address_bar(self):
           """Focus the address bar."""

           self.address_bar.setFocus()
           self.address_bar.selectAll()

    def update_address_bar(self, url):
           print("Navigating to:", url.toString())

           if url.isLocalFile():
                self.address_bar.setText("vanadium://home")
                return

           self.address_bar.setText(url.toString())

    def open_settings(self):
           dialog = SettingsDialog()
           dialog.exec()

    def navigate_to_text(self, text):
           """Navigate to a website or search query."""

           text = text.strip()

           if not text:
                return

    # Website
           if "." in text:
                if not text.startswith(("http://", "https://")):
                     text = "https://" + text

                url = QUrl(text)

    # Search
           else:
                settings = load_settings()
                engine = settings.get("search_engine", "bing")

                query = text.replace(" ", "+")


                if engine == "bing":
                     search_url = f"https://www.bing.com/search?q={query}"

                elif engine == "duckduckgo":
                     search_url = f"https://duckduckgo.com/?q={query}"

                else:
                     search_url = f"https://www.google.com/search?q={query}"

                url = QUrl(search_url)

           self.tabs.current_browser().setUrl(url)

    def add_bookmark(self):

           browser = self.tabs.current_browser()

           if browser is None:
                return

           title = browser.title()

           url = browser.url().toString()

           self.bookmarks.add_bookmark(title, url)

           self.statusBar().showMessage(
                "Bookmark added!",
                 3000
           )

    def refresh_bookmarks(self):
           """Refresh the bookmarks menu."""

           self.bookmarks_menu.clear()

           for bookmark in self.bookmarks.all_bookmarks():

                action = self.bookmarks_menu.addAction(bookmark["title"])

                action.triggered.connect(
                     lambda checked=False, url=bookmark["url"]:
                     self.tabs.current_browser().setUrl(QUrl(url))
                )


    def open_history(self):
           """Open the browsing history."""

           dialog = HistoryDialog(self.history, self)
           dialog.exec()

    def handle_download(self, download):
           """Handle a new download request."""

           filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                download.downloadFileName()
           )

           if not filename:
                download.cancel()
                return

           download.setDownloadDirectory(
                str(Path(filename).parent)
           )

           download.setDownloadFileName(
                Path(filename).name
           )
           self.active_downloads.append(download)

           download.accept()

           download.receivedBytesChanged.connect(
                lambda: self.download_progress(download)
           )

           download.isFinishedChanged.connect(
                lambda: self.download_finished(download)
           )

    def download_progress(self, download):
           """Track download progress."""

           received = download.receivedBytes()
           total = download.totalBytes()

           if total > 0:
                percent = int(received * 100 / total)
                self.statusBar().showMessage(
                     f"Downloading... {percent}%"
                )

    def download_finished(self, download):
           """Called when a download finishes."""

           path = str(
                Path(download.downloadDirectory()) /
                download.downloadFileName()
           )

           self.download_manager.add_download(
                download.downloadFileName(),
                path,
                "Completed"
           )

           self.statusBar().showMessage(
                "Download complete!",
                3000
          )

           if download in self.active_downloads:
                self.active_downloads.remove(download)

    def open_downloads(self):
           """Open the downloads window."""

           dialog = DownloadsDialog(
                self.download_manager,
                self
           )

           dialog.exec()