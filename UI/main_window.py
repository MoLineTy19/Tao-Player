import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QApplication, QFileDialog, QHBoxLayout
)
import config.gradient
from styles.main_window import default_text


class TaoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.startPos = None
        self.default_coordinates = (300, 200, 1280, 720)

        # Инициализация медиаплеера и виджета видео
        self.media_player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.video_widget = QVideoWidget()
        self.setup_video_widget()

        self.media_player.setAudioOutput(self.audio)
        self.media_player.setVideoOutput(self.video_widget)

        self.init_ui()
        self.set_position()

    def setup_video_widget(self):
        """Настройка виджета видео."""
        self.video_widget.setMinimumWidth(1280)
        self.video_widget.setMinimumHeight(525)

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(config.gradient.gradient_brown)  # Фон для основного виджета
        self.setWindowTitle('Tao Player')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addLayout(self.setup_header_service_menu())
        layout.addWidget(self.video_widget)
        layout.addWidget(self.setup_menu_control_video(), alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)

    def set_position(self):
        """Установка позиции окна на экране."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        if screen_rect.width() >= 1920:
            self.setGeometry(*self.default_coordinates)

    def setup_menu_control_video(self):
        """Создание меню управления."""
        menu_label = self.create_label("МЕНЮ УПРАВЛЕНИЯ", 155)
        return menu_label

    def setup_header_service_menu(self):
        """Создание шапки с вложенным QHBoxLayout."""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Внутренний QHBoxLayout
        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(10)  # Установите нужное расстояние между элементами

        # Иконка
        icon = QLabel()
        pixmap = QPixmap("logo.jpg")  # Замените на путь к вашему изображению
        icon.setPixmap(pixmap)
        icon.setMaximumHeight(40)  # Ограничиваем высоту иконки

        # Название плеера
        name_player = QLabel('<span style="color: red;">Tao</span> <span style="color: white;">Player</span>')
        name_player.setStyleSheet(default_text + "font-size: 20px; font-weight: bold;")  # Жирный шрифт

        # Версия плеера
        version = QLabel("v1.0")
        version.setStyleSheet(default_text + "font-size: 16px; font-weight: bold;")  # Жирный шрифт

        # Добавляем элементы во внутренний layout
        inner_layout.addWidget(name_player)
        inner_layout.addWidget(icon)
        inner_layout.addWidget(version)

        # Добавляем внутренний layout в основной layout
        header_layout.addLayout(inner_layout)

        return header_layout

    def create_label(self, text, height):
        """Создание метки."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(height)
        return label

    def create_button(self, text):
        """Создание кнопки."""
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(self.on_button_clicked)
        return button

    def mousePressEvent(self, event):
        """Обработка нажатия мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Обработка перемещения мыши."""
        if self.startPos is not None:
            self.move(event.globalPosition().toPoint() - self.startPos)

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = None

    def on_button_clicked(self):
        """Обработка нажатия кнопки загрузки видео."""
        video_file, _ = QFileDialog.getOpenFileName(self, "Выберите видео файл", "", "Video Files (*.mp4 *.avi *.mkv)")
        if video_file:
            self.load_video(video_file)

    def load_video(self, video_file):
        """Загрузка и воспроизведение видео."""
        print(f"Выбран файл: {video_file}")  # Отладочное сообщение
        self.media_player.setSource(QUrl.fromLocalFile(video_file))
        self.media_player.play()  # Запускаем воспроизведение
        print("Воспроизведение видео начато.")
