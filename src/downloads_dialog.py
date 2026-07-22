from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout
)
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class DownloadsDialog(QDialog):

    def __init__(self, download_manager, parent=None):
        super().__init__(parent)

        self.download_manager = download_manager

        self.setWindowTitle("Downloads")
        self.resize(600, 450)

        self.setup_ui()
        self.load_downloads()
        self.download_list.itemDoubleClicked.connect(
             self.open_download
        )

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("⬇ Downloads")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.download_list = QListWidget()
        layout.addWidget(self.download_list)

        buttons = QHBoxLayout()

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(
             self.clear_downloads
        )
        self.close_button = QPushButton("Close")

        buttons.addWidget(self.clear_button)
        buttons.addStretch()
        buttons.addWidget(self.close_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.close_button.clicked.connect(self.close)
    
    def load_downloads(self):
        self.download_list.clear()

        for item in reversed(self.download_manager.all_downloads()):
            self.download_list.addItem(
                f"{item['filename']}\n{item['status']}"
            )

    def open_download(self, item):
         """Open the selected downloaded file."""

         filename = item.text().split("\n")[0]

         for download in self.download_manager.all_downloads():

             if download["filename"] == filename:

                 QDesktopServices.openUrl(
                     QUrl.fromLocalFile(download["path"])
                 )

                 break
             
    def clear_downloads(self):
         """Clear the download history."""

         self.download_manager.clear()

         self.load_downloads()