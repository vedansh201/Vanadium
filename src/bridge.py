import json
from pathlib import Path
import json
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

    @pyqtSlot(result=str)
    def getWallpaper(self):
        """Return the current wallpaper path."""
        from pathlib import Path
        import json

        settings_file = (
             Path(__file__).parent.parent /
             "settings.json"
         )

        if not settings_file.exists():
             return ""

        with open(settings_file, "r") as file:
             settings = json.load(file)

        return settings.get("wallpaper", "")
        