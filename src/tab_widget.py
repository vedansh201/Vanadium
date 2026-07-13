from PyQt6.QtWidgets import( QTabWidget, QPushButton )
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QUrl, pyqtSignal

class BrowserTabs(QTabWidget):
    """Manages all browser tabs."""
    

    url_changed = pyqtSignal(QUrl)
    title_changed = pyqtSignal(str)
    load_started = pyqtSignal()
    load_progress = pyqtSignal(int)
    load_finished = pyqtSignal(bool)
    def __init__(self):
        super().__init__()

        self.setup_tabs()
        self.create_tab()

    def setup_tabs(self):
        """Configure the tab widget."""

        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setCornerWidget(None)
        add_tab_button = QPushButton("+")
        add_tab_button.setFixedWidth(28)
        self.currentChanged.connect(self.tab_changed)
        self.currentChanged.connect(self.current_tab_changed)
        add_tab_button.clicked.connect(self.create_tab)

        self.setCornerWidget(add_tab_button)

    def create_tab(self, url=None):
         """Create a new browser tab."""

         browser = QWebEngineView()

       # Connect browser signals
         browser.urlChanged.connect(self.url_changed)
         browser.titleChanged.connect(self.title_changed)
         browser.loadStarted.connect(self.load_started)
         browser.loadProgress.connect(self.load_progress)
         browser.loadFinished.connect(self.load_finished)
         browser.titleChanged.connect(
              lambda title, browser=browser: self.update_tab_title(browser, title)
        )

        # Default homepage
         if url is None:
             url = QUrl("https://duckduckgo.com")

         browser.setUrl(url)

        # Insert tab next to the current tab
         current_index = self.currentIndex()

         if current_index == -1:
             index = self.addTab(browser, "New Tab")
         else:
             index = current_index + 1
             self.insertTab(index, browser, "New Tab")

         # Switch to the new tab
         self.setCurrentIndex(index)

         return browser

    def current_browser(self):
        """Return the browser in the current tab."""
        return self.currentWidget()

    def close_tab(self, index):
         """Close a browser tab."""

         browser = self.widget(index)

         self.removeTab(index)

         browser.deleteLater()

         # Never leave the browser without a tab
         if self.count() == 0:
             self.create_tab()
             
    def tab_changed(self, index):
         browser = self.current_browser()

         if browser:
             self.url_changed.emit(browser.url())
             self.title_changed.emit(browser.title())

    def update_tab_title(self, browser, title):
         """Update the title of a browser tab."""

         index = self.indexOf(browser)

         if index == -1:
             return

         if not title:
             title = "New Tab"

       # Keep titles short
         if len(title) > 20:
             title = title[:20] + "..."

         self.setTabText(index, title)

    def current_tab_changed(self, index):
         """Called whenever the active tab changes."""

         browser = self.current_browser()

         if browser:
             self.url_changed.emit(browser.url())
             self.title_changed.emit(browser.title())