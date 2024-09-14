import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QSplitter, QVBoxLayout, QSizePolicy

from config import gradient_brown


class TaoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Настройка окна
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle('Tao Player')
        self.setGeometry(300, 200, 1280, 720)

        # Создаем основной компоновщик
        menu_control = QVBoxLayout()
        menu_control.setContentsMargins(0, 0, 0, 0)

        # название
        menu_label = QLabel(text="МЕНЮ УПРАВЛЕНИЯ")
        # расположение
        menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        # цвет
        menu_label.setStyleSheet(gradient_brown)
        # ширина
        menu_label.setFixedHeight(155)

        menu_service = QVBoxLayout()
        menu_service.setContentsMargins(0, 0, 0, 0)

        menu_service_label = QLabel(text="СЕРВИС")
        menu_service_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        menu_service_label.setStyleSheet(gradient_brown)
        menu_service_label.setFixedHeight(40)

        menu_service.addWidget(menu_service_label, alignment=Qt.AlignmentFlag.AlignTop)
        menu_control.addLayout(menu_service)

        menu_control.addWidget(menu_label, alignment=Qt.AlignmentFlag.AlignBottom)
        self.setLayout(menu_control)

        button = QPushButton("Нажми меня")
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(self.on_button_clicked)  # Подключаем слот
        # Добавляем кнопку в компоновщик
        menu_service.addWidget(button)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            self.move(event.globalPosition().toPoint() - self.startPos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = None

    def resizeEvent(self, event):
        # Обработка изменения размера (если необходимо)
        super().resizeEvent(event)

    def on_button_clicked(self):
        print("Кнопка нажата!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaoApp()
    window.show()
    sys.exit(app.exec())
