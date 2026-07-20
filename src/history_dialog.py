from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QUrl



class HistoryDialog(QDialog):

    def __init__(self, history_manager, parent=None):
        super().__init__(parent)

        self.history_manager = history_manager

        self.setWindowTitle("Browsing History")
        self.resize(600, 450)

        self.setup_ui()
        self.load_history()
        self.history_list.itemDoubleClicked.connect(
             self.open_history_item
        )
        self.clear_button.clicked.connect(
             self.clear_history
        )
        
    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("📜 Browsing History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        buttons = QHBoxLayout()

        self.clear_button = QPushButton("Clear History")
        self.close_button = QPushButton("Close")

        buttons.addWidget(self.clear_button)
        buttons.addStretch()
        buttons.addWidget(self.close_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.close_button.clicked.connect(self.close)

    def load_history(self):

        self.history_list.clear()

        for item in reversed(self.history_manager.all_history()):

             self.history_list.addItem(
                 f"{item['title']}\n{item['url']}"
            )
             
    def open_history_item(self, item):
         """Open the selected history entry."""

         url = item.text().split("\n")[1]

         self.parent().tabs.current_browser().setUrl(QUrl(url))

         self.close()

    def clear_history(self):

         self.history_manager.clear()

         self.load_history()