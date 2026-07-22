from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
    QFileDialog,
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


        appearance_group = QGroupBox("Appearance")

        appearance_layout = QVBoxLayout()

        self.light_radio = QRadioButton("☀ Light")
        self.dark_radio = QRadioButton("🌙 Dark")

        self.light_radio.setChecked(True)

        appearance_layout.addWidget(self.light_radio)
        appearance_layout.addWidget(self.dark_radio)

        appearance_group.setLayout(appearance_layout)

        layout.addWidget(appearance_group)


        homepage_group = QGroupBox("Homepage")

        
        homepage_layout = QVBoxLayout()

        self.wallpaper_label = QLabel("Current: Default")

        self.wallpaper_button = QPushButton("🖼 Choose Wallpaper")

        self.wallpaper_button.clicked.connect(self.choose_wallpaper)

        homepage_layout.addWidget(self.wallpaper_label)
        homepage_layout.addWidget(self.wallpaper_button)

        homepage_group.setLayout(homepage_layout)

        layout.addWidget(homepage_group)
        
        self.wallpaper_button.clicked.connect(self.choose_wallpaper)
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

         settings_file = (
             Path(__file__).parent.parent /
             "settings.json"
         )

         # Load existing settings if they exist
         if settings_file.exists():
             with open(settings_file, "r") as file:
                 settings = json.load(file)
         else:
             settings = {}

         # Update settings
         settings["search_engine"] = search_engine

         
         
         if self.dark_radio.isChecked():
             settings["theme"] = "dark"
         else:
             settings["theme"] = "light"

    # Save wallpaper if one was selected
         if hasattr(self, "wallpaper_path"):
             settings["wallpaper"] = self.wallpaper_path
 
         with open(settings_file, "w") as file:
             json.dump(settings, file, indent=4)

         self.accept()

        

    def load_settings(self):
         """Load saved settings."""

         settings_file = (
             Path(__file__).parent.parent /
             "settings.json"
         )

    # If no settings file exists, use defaults
         if not settings_file.exists():
             self.wallpaper_path = ""
             self.wallpaper_label.setText("Current: Default")
             return

    # Load the JSON first
         with open(settings_file, "r") as file:
             settings = json.load(file)

    # NOW you can use 'settings'
         self.wallpaper_path = settings.get("wallpaper", "")

         engine = settings.get("search_engine", "bing")

         if engine == "bing":
             self.bing_radio.setChecked(True)
         elif engine == "duckduckgo":
             self.ddg_radio.setChecked(True)
         else:
             self.google_radio.setChecked(True)

         theme = settings.get("theme", "light")

         if theme == "dark":
             self.dark_radio.setChecked(True)
         else:
             self.light_radio.setChecked(True)

         if self.wallpaper_path:
             self.wallpaper_label.setText(
                 f"Current: {Path(self.wallpaper_path).name}"
             )
         else:
             self.wallpaper_label.setText("Current: Default")

    def choose_wallpaper(self):
        filename, _ = QFileDialog.getOpenFileName(
             self,
             "Choose Wallpaper",
             "",
             "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if filename:
             self.wallpaper_path = filename
             self.wallpaper_label.setText(
                 f"Current: {Path(filename).name}"
             )