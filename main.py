import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle('Пример PyQt6')
        self.setGeometry(100, 100, 300, 200)

        # Создание кнопки
        self.button = QPushButton('Нажми меня', self)
        self.button.setGeometry(100, 70, 100, 30)
        self.button.clicked.connect(self.show_message)

    def show_message(self):
        QMessageBox.information(self, 'Сообщение', 'Кнопка нажата!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
