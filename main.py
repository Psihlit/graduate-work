import sys

from PyQt6.QtWidgets import QApplication
from UI.StartViews import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow(current_user=None)
    window.show()
    sys.exit(app.exec())
