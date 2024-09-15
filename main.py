import sys
from PyQt6.QtWidgets import QApplication
from UI.main_window import TaoApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaoApp()
    window.show()
    sys.exit(app.exec())
