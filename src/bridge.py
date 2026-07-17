from PyQt6.QtCore import QObject, pyqtSlot


class BrowserBridge(QObject):
    """Bridge between JavaScript and Python."""

    def __init__(self, browser_window):
        super().__init__()

        self.browser_window = browser_window

    @pyqtSlot(str)
    def search(self, text):
        """Called from JavaScript."""

        self.browser_window.navigate_to_text(text)