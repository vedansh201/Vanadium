import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vanadium")
        self.resize(1280, 720)


app = QApplication(sys.argv)

window = BrowserWindow()
window.show()

sys.exit(app.exec())
