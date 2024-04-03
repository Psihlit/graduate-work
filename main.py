import sys
from PyQt6.QtWidgets import QApplication
from UI.Views import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())