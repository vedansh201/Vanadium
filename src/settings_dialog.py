from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
)
import json
from pathlib import Path

class SettingsDialog(QDialog):
    """Settings window for Vanadium."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vanadium Settings")
        self.resize(500, 400)

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("⚙ Vanadium Settings")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        # ----------------------------
        # Homepage Settings
        # ----------------------------
        homepage_group = QGroupBox("Homepage")

        homepage_layout = QVBoxLayout()

        self.wallpaper_button = QPushButton("🖼 Change Background")

        homepage_layout.addWidget(self.wallpaper_button)

        homepage_group.setLayout(homepage_layout)

        layout.addWidget(homepage_group)

        # ----------------------------
        # Search Engine
        # ----------------------------
        search_group = QGroupBox("Default Search Engine")

        search_layout = QVBoxLayout()

        self.bing_radio = QRadioButton("Bing")
        self.ddg_radio = QRadioButton("DuckDuckGo")
        self.google_radio = QRadioButton("Google")

        self.bing_radio.setChecked(True)

        search_layout.addWidget(self.bing_radio)
        search_layout.addWidget(self.ddg_radio)
        search_layout.addWidget(self.google_radio)

        search_group.setLayout(search_layout)

        layout.addWidget(search_group)

        # ----------------------------
        # Bottom Buttons
        # ----------------------------
        buttons = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton("Cancel")

        buttons.addStretch()
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        # Close dialog
        self.cancel_button.clicked.connect(self.close)
    def save_settings(self):
         """Save the user's settings."""

         if self.bing_radio.isChecked():
             search_engine = "bing"

         elif self.ddg_radio.isChecked():
             search_engine = "duckduckgo"

         else:
             search_engine = "google"

         settings = {
             "search_engine": search_engine
         }

         settings_file = (
             Path(__file__).parent.parent /
             "settings.json"
         )

         with open(settings_file, "w") as file:
             json.dump(settings, file, indent=4)

         self.accept()

    def load_settings(self):
         """Load saved settings."""

         settings_file = (
             Path(__file__).parent.parent /
             "settings.json"
         )

         if not settings_file.exists():
             return

         with open(settings_file, "r") as file:
             settings = json.load(file)

         engine = settings.get("search_engine", "bing")

         if engine == "bing":
             self.bing_radio.setChecked(True)

         elif engine == "duckduckgo":
             self.ddg_radio.setChecked(True)

         elif engine == "google":
             self.google_radio.setChecked(True)