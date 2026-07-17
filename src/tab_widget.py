from PyQt6.QtWidgets import( QTabWidget, QPushButton )
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QUrl, pyqtSignal
from pathlib import Path
from PyQt6.QtWebChannel import QWebChannel

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

    def setup_tabs(self):
         """Configure the tab widget."""

         self.setDocumentMode(True)
         self.setTabsClosable(True)
         self.setMovable(True)

         self.tabCloseRequested.connect(self.close_tab)

         self.add_tab_button = QPushButton("+")
         self.add_tab_button.setFixedWidth(28)

         self.setCornerWidget(self.add_tab_button)

         self.currentChanged.connect(self.tab_changed)
         self.currentChanged.connect(self.current_tab_changed)

    def create_tab(self, url=None, channel=None):
         """Create a new browser tab."""

         if not isinstance(url, QUrl):
             url = None

         browser = QWebEngineView()
         if channel is not None:
             browser.page().setWebChannel(channel)

       # Connect browser signals
         browser.urlChanged.connect(self.url_changed)
         browser.titleChanged.connect(self.title_changed)
         browser.loadStarted.connect(self.load_started)
         browser.loadProgress.connect(self.load_progress)
         browser.loadFinished.connect(self.load_finished)
         browser.titleChanged.connect(
              lambda title, browser=browser: self.update_tab_title(browser, title)
        )
         browser.iconChanged.connect(
              lambda icon, browser=browser: self.update_tab_icon(browser, icon)
        )
         
         browser.loadStarted.connect(
              lambda browser=browser: self.tab_loading_started(browser)
        )

         browser.loadFinished.connect(
              lambda _, browser=browser: self.tab_loading_finished(browser)
        )
        # Default homepage
         if url is None:
              home_page = (Path(__file__).parent.parent / "assets" / "home" / "home.html").resolve()

              url = QUrl.fromLocalFile(str(home_page))

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

         full_title = title

         if not title:
             title = "New Tab"

         display_title = title

         if len(display_title) > 20:
             display_title = display_title[:20] + "..."

         self.setTabText(index, display_title)
         self.setTabToolTip(index, full_title)

    def current_tab_changed(self, index):
         """Called whenever the active tab changes."""

         browser = self.current_browser()

         if browser:
             self.url_changed.emit(browser.url())
             self.title_changed.emit(browser.title())

    def update_tab_icon(self, browser, icon):
         """Update the favicon of a browser tab."""

         index = self.indexOf(browser)

         if index != -1:
             self.setTabIcon(index, icon)

    def tab_loading_started(self, browser):
         """Show loading text while a page is loading."""

         index = self.indexOf(browser)

         if index != -1:
             self.setTabText(index, "Loading...")

    def tab_loading_finished(self, browser):
         """Restore the page title after loading."""

         index = self.indexOf(browser)

         if index != -1:
             title = browser.title()

             if not title:
                 title = "New Tab"

             if len(title) > 20:
                 title = title[:20] + "..."

             self.setTabText(index, title)